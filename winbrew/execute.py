import itertools
import argparse
import sys
import os
import errno
import subprocess

import winbrew
import winbrew.util

class InstallException(Exception):
    pass

class InstallPlan:
    """
    Executes a topological sort to determine the order in which to install
    packages.
    """
    def __init__(self, formulas, args):
        self.args = args
        self.order = []
        self.preinstalled = []
        self.marked = set()
        self.temp = set()
        self.forced = set(formulas) if self.args.force else set()

        for formula in formulas:
            self.visit(formula)

    def visit(self, formula):
        """
        Visit the node with the given name and all children in a depth-first
        search.
        """
        if formula.name in self.temp:
            raise InstallException('circular dependency')
        if formula.name not in self.marked:
            self.temp.add(formula.name)
            for dep_name in itertools.chain(formula.deps, formula.build_deps):
                dep = winbrew.Formula.formula_by_name(dep_name)()
                self.visit(dep)
            self.temp.remove(formula.name)
            self.marked.add(formula.name)
            if formula in self.forced or not formula.manifest.installed:
                # Only install a package if it's not already installed
                self.order.append(formula)
            else:
                self.preinstalled.append(formula)

    def __iter__(self):
        """
        Returns a list of packages to be installed in dependency-order, or
        throws an exception if there are circular dependencies.
        """
        return iter(self.order)

    def setenv(self):
        """
        Set up install environment
        """
        os.environ.update({
            'INCLUDE': os.pathsep.join((
                os.environ['INCLUDE'],
                winbrew.sdk_include_path,
                winbrew.include_path,
            )),
            'LIBPATH': os.pathsep.join((
                os.environ['LIBPATH'],
                winbrew.sdk_lib_path,
                winbrew.lib_path)),
            'LIB': os.pathsep.join((
                os.environ['LIB'],
                winbrew.sdk_lib_path,
                winbrew.lib_path,
            )),
            'PATH': os.pathsep.join((
                os.environ['PATH'],
                winbrew.sdk_bin_path,
                winbrew.bin_path
            )),
        })

    def execute(self):
        """
        Install all packages in the install plan
        """
        self.setenv()

        for formula in self.preinstalled:
            print(('%s already installed' % formula.name))

        self.download()
        self.build()
        self.install()

    def download(self):
        if self.args.skip_download: return

        for formula in self:
            formula.download()
            formula.clean()
            formula.verify()
        for formula in self:
            formula.unpack()

    def build(self):
        if self.args.skip_build: return

        for formula in self:
            formula.setenv()
            formula.build()

    def install(self):
        if self.args.skip_install: return

        for formula in self:
            formula.setenv()
            formula.install()
            formula.manifest.save()

def uninstall(args):
    """
    Uninstall a package.  FIXME: Eventually, this should uninstall packages
    that depend on this package.  For now, just nuke the installed files.
    """
    for name in args.package:
        formula = winbrew.Formula.formula_by_name(name)()
        if not args.force and not formula.manifest.installed:
            print(('%s is not installed' % formula.name))
            continue
        formula.manifest.load()
        for fn in formula.manifest.files:
            try:
                os.remove(fn)
            except OSError as e:
                pass
            # Clean up parent directories if empty
            while True:
                fn, end = os.path.split(fn)
                try:
                    os.rmdir(fn)
                except OSError as e:
                    break
        formula.manifest.delete()

def test(args):
    """
    Test a package.
    """
    for name in args.package:
        formula = winbrew.Formula.formula_by_name(name)()
        formula.test()
    print('PASS')

def listp(args):
    """
    List package contents
    """
    for name in args.package:
        formula = winbrew.Formula.formula_by_name(name)()
        formula.manifest.load()
        print(('\n'.join(formula.manifest.files)))

def update(args):
    """
    Update by cloning formulas from the git repository.
    """
    os.chdir(winbrew.home)
    cmd = ('git', 'pull')
    subprocess.check_call(cmd, shell=True)

def formula_from_args(args, name):
    """
    Parse formulas/formula arguments.
    """
    formula = winbrew.Formula.formula_by_name(name)()
    args = formula.parse_options(args)
    return (formula, args)

def download(args):
    """
    Download a formula, but don't unpack or install it
    """
    for name in args.package:
        formula = winbrew.Formula.formula_by_name(name)()
        formula.download()
        formula.verify()

def install(args):
    """
    Install a package and dependencies.
    """
    package = args.package
    try:
        formulas = []
        while len(package) > 0:
            name = package.pop(0)
            (formula, package) = formula_from_args(package, name)
            formulas.append(formula)
        InstallPlan(formulas, args).execute()
    except InstallException as e:
        sys.stderr.write('error: %s\n' % str(e))
        sys.exit(1)

def reinstall(args):
    """
    Reinstall packages
    """
    package = args.package
    if args.all:
        package += [manifest.name for manifest in winbrew.Manifest.all()]

    args.force = True
    try:
        formulas = []
        while len(package) > 0:
            name = package.pop(0)
            (formula, package) = formula_from_args(package, name)
            formulas.append(formula)
        InstallPlan(formulas, args).execute()
    except InstallException as e:
        sys.stderr.write('error: %s\n' % str(e))
        sys.exit(1)

def edit(args):
    """
    Edit a package.
    """
    path = os.path.join(winbrew.formula_path, '%s.py' % args.name)
    if not os.path.exists(path):
        sys.stderr.write('error: file formula not found: %s\n' % args.name)
        sys.exit(1)

    editor = os.environ.get('EDITOR', 'notepad')
    try:
        subprocess.check_call((editor, path), shell=True)
    except subprocess.CalledProcessError as e:
        pass
    except SystemError as e:
        sys.stderr.write('error: %s\n' % str(e))
        sys.stderr.flush()
        sys.exit(1)

def create(args):
    """
    Create a new package.
    """
    base = os.path.split(args.url)[1]
    base = base.split('.')[0]
    base = base.split('-')[0]
    base = base.split('_')[0]
    name = args.name or base

    template = """
import winbrew

class %(name)s(winbrew.Formula):
    url = '%(url)s'
    homepage = ''
    sha1 = ''
    build_deps = ()
    deps = ()

    def install(self):
        pass

    def test(self):
        pass
"""

    path = os.path.join(winbrew.formula_path, '%s.py' % name)
    if not os.path.exists(path):
        winbrew.util.mkdir_p(os.path.split(path)[0])
        fd = open(path, 'w')
        fd.write(template % {'name': name.title(), 'url': args.url})
        fd.close()

    args.name = name
    edit(args)

def freeze(args):
    """
    Output installed packages.
    """
    print(('\n'.join([manifest.name for manifest in winbrew.Manifest.all()])))

def init():
    if not os.path.exists(os.path.join(winbrew.home, '.git')):
        cmd = ('git', 'clone', winbrew.formula_url, winbrew.home)
        print((' '.join(cmd)))
        subprocess.check_call(cmd, shell=True)

def main():
    parser = argparse.ArgumentParser(prog='winbrew', description='Package installer for Windows')
    subparsers = parser.add_subparsers(dest='command')

    sub = subparsers.add_parser('create', help='create a new package')
    sub.add_argument('url', type=str, help='package source URL')
    sub.add_argument('-n', '--name', type=str, help='package name', default=None)

    sub = subparsers.add_parser('edit', help='edit a package')
    sub.add_argument('name', type=str, help='package source name')

    sub = subparsers.add_parser('install', help='install packages')
    sub.add_argument('--force', '-f', action='store_true', help='force package install (completely reinstall it)')
    sub.add_argument('--skip-download', action='store_true', help='skip download step')
    sub.add_argument('--skip-build', action='store_true', help='skip build step')
    sub.add_argument('--skip-install', action='store_true', help='skip install step')
    sub.add_argument('package', type=str, nargs=argparse.REMAINDER, help='packages to install')

    sub = subparsers.add_parser('reinstall', help='reinstall packages')
    sub.add_argument('--all', '-a', action='store_true', help='reinstall all packages')
    sub.add_argument('package', type=str, nargs=argparse.REMAINDER, help='packages to reinstall')

    sub = subparsers.add_parser('uninstall', help='uninstall packages')
    sub.add_argument('--force', '-f', action='store_true', help='force package uninstall')
    sub.add_argument('package', type=str, nargs='+', help='packages to uninstall')

    sub = subparsers.add_parser('list', help='list package contents')
    sub.add_argument('package', type=str, nargs='+', help='packages to list')

    sub = subparsers.add_parser('test', help='test packages')
    sub.add_argument('package', type=str, nargs=argparse.REMAINDER, help='packages to test')

    sub = subparsers.add_parser('freeze', help='output installed packages')

    sub = subparsers.add_parser('update', help='update formulas from server')

    sub = subparsers.add_parser('download', help='download formulas without installing them')
    sub.add_argument('package', type=str, nargs=argparse.REMAINDER, help='packages to download')

    args = parser.parse_args()

    try:
        init()

        if args.command == 'create':
            create(args)
        elif args.command == 'edit':
            edit(args)
        elif args.command == 'install':
            install(args)
        elif args.command == 'reinstall':
            reinstall(args)
        elif args.command == 'uninstall':
            uninstall(args)
        elif args.command == 'update':
            update(args)
        elif args.command == 'test':
            test(args)
        elif args.command == 'list':
            listp(args)
        elif args.command == 'freeze':
            freeze(args)
        elif args.command == 'download':
            download(args)
        else:
            sys.stderr.write('error: unknown command')
            sys.exit(1)
    except winbrew.FormulaException as e:
        sys.stderr.write('error: %s\n' % str(e))
        sys.stderr.flush()
        sys.exit(1)


if __name__ == '__main__':
    main()




