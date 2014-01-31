import winbrew 
import itertools
import argparse
import sys
import os
import subprocess

class InstallException(Exception):
    pass

class InstallPlan:
    """
    Executes a topological sort to determine the order in which to install
    packages.
    """
    def __init__(self, formulas):
        self.marked = set()
        self.temp = set()
        self.order = []
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
            self.order.append(formula)

    def __iter__(self):
        """
        Returns a list of packages to be installed in dependency-order, or
        throws an exception if there are circular dependencies.
        """
        return iter(self.order)

    def execute(self):
        """
        Install all packages in the install plan
        """
        os.environ['PATH'] = os.pathsep.join((
            os.environ['PATH'], 
            winbrew.bin_path,
        ))
        for formula in self:
            formula.download()
        for formula in self:
            formula.unpack()
        for formula in self:
            formula.setup()
            formula.manifest.save()

def uninstall(args):
    """
    Uninstall a package.  FIXME: Eventually, this should uninstall packages
    that depend on this package.  For now, just nuke the installed files.
    """
    for name in args.package:
        formula = winbrew.Formula.formula_by_name(name)()
        formula.manifest.load()
        for fn in formula.manifest.files:
            try:
                print('removing %s' % fn)
                os.remove(fn)
            except OSError, e:
                pass

def update(args):
    """
    Update by cloning formulas from the git repository.
    """
    if not os.path.exists(winbrew.home):
        cmd = ('git', 'clone', winbrew.formula_url, winbrew.home)
        subprocess.check_call(cmd, shell=True)
    else:
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

def install(args):
    package = args.package
    try:
        formulas = []
        while len(package) > 0:
            name = package.pop(0)
            (formula, package) = formula_from_args(package, name)
            formulas.append(formula)
        InstallPlan(formulas).execute()
    except InstallException, e:
        sys.stderr.write('error: %s\n' % str(e))
        sys.exit(1)
             
def main():
    parser = argparse.ArgumentParser(prog='winbrew', description='Package installer for Windows')
    subparsers = parser.add_subparsers(dest='command')

    sub = subparsers.add_parser('install', help='Install packages')
    sub.add_argument('package', type=str, nargs=argparse.REMAINDER, help='Packages to install')

    sub = subparsers.add_parser('uninstall', help='Uninstall packages')
    sub.add_argument('package', type=str, nargs='+', help='Packages to uninstall')

    sub = subparsers.add_parser('update', help='Update formulas from server')

    args = parser.parse_args()

    try:
        if args.command == 'install':
            install(args)
        elif args.command == 'uninstall':
            uninstall(args)
        elif args.command == 'update':
            update(args)
        else:
            sys.stderr.write('error: unknown command')
            sys.exit(1)
    except winbrew.FormulaException, e:
        sys.stderr.write('error: %s\n' % str(e))
        sys.stderr.flush()
        sys.exit(1)
        
    
if __name__ == '__main__':
    main()




