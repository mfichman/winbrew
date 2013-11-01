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

    def visit(self, name):
        """
        Visit the node with the given name and all children in a depth-first
        search.  
        """
        if name in self.temp:
            raise InstallException('circular dependency')
        if name not in self.marked:
            formula = winbrew.Formula.formula_by_name(name)
            self.temp.add(name)
            for dep in itertools.chain(formula.deps, formula.build_deps):
                self.visit(dep) 
            self.temp.remove(name)
            self.marked.add(name)
            self.order.append(formula())

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
        #os.environ['PATH'] = os.pathsep.join(os.environ['PATH'], 
        for formula in self:
            formula.download()
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
    print winbrew.formula_path
    if not os.path.exists(winbrew.formula_path):
        cmd = ('git', 'clone', winbrew.formula_url, winbrew.formula_path)
        subprocess.check_call(cmd, shell=True)
    else:
        os.chdir(winbrew.formula_path)
        cmd = ('git', 'pull')
        subprocess.check_call(cmd, shell=True)

def install(args):
    try:
        InstallPlan(args.package).execute()
    except InstallException, e:
        sys.stderr.write('error: %s\n' % str(e))
        sys.exit(1)
             
def main():
    parser = argparse.ArgumentParser(prog='winbrew', description='Package installer for Windows')
    parser.prog
    subparsers = parser.add_subparsers(dest='command')

    sub = subparsers.add_parser('install', help='install packages')
    sub.add_argument('package', type=str, nargs='+', help='packages to install')

    sub = subparsers.add_parser('uninstall', help='install packages')
    sub.add_argument('package', type=str, nargs='+', help='packages to install')

    sub = subparsers.add_parser('update', help='update formulas')

    args = parser.parse_args()

    if args.command == 'install':
        install(args)
    elif args.command == 'uninstall':
        uninstall(args)
    elif args.command == 'update':
        update(args)
    else:
        sys.stderr.write('error: unknown command')
        sys.exit(1)
        
    
if __name__ == '__main__':
    main()



