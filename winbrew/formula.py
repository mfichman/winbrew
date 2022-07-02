import subprocess
import sys
import os
import errno
import glob
import shutil
import shlex
import imp
import winbrew
import argparse
import hashlib
import re
import patch

import winbrew
import winbrew.util
from winbrew.manifest import Manifest
from winbrew.archive import Archive

# Default arguments for the supported build tools
cmake_args = ('-G', 'Visual Studio 17 2022', '-A', 'x64')
msbuild_args = ('/P:Configuration=Release', '/p:PlatformToolset=v143', '/p:UseEnv=true')

class FormulaException(Exception):
    pass

class FormulaProxy:
    def __init__(self, formula):
        self.formula = formula

    @property
    def name(self):
        return self.formula.name

    @property
    def deps(self):
        return self.formula.deps

    @property
    def manifest(self):
        return self.formula.manifest

    @property
    def build_deps(self):
        return self.formula.build_deps

    def parse_options(self, args):
        return self.formula.parse_options(args)

    def download(self, force=False):
        if self.formula.manifest.status != 'uninstalled' and not force: return
        print(('downloading %s' % self.name))
        self.formula.download()
        self.formula.verify()
        self.formula.manifest.status = 'downloaded'
        self.formula.manifest.save()

    def unpack(self):
        if self.formula.manifest.status != 'downloaded': return
        print(('unpacking %s' % self.name))
        self.formula.setenv()
        self.formula.unpack()
        self.formula.setenv()
        self.formula.patch()
        self.formula.manifest.status = 'unpacked'
        self.formula.manifest.save()

    def build(self, force=False):
        if self.formula.manifest.status != 'unpacked': return
        print(('building %s' % self.name))
        self.formula.setenv()
        self.formula.build()
        self.formula.manifest.status = 'built'
        self.formula.manifest.save()

    def install(self, force=False):
        if self.formula.manifest.status != 'built' and not force:
            print(('%s already installed' % self.formula.name))
            return
        print(('installing %s' % self.name))
        self.formula.setenv()
        self.formula.install()
        self.formula.manifest.status = 'installed'
        self.formula.manifest.save()

    def uninstall(self, force=False):
        if self.formula.manifest.status != 'installed' and not force:
            print(('%s not installed' % self.formula.name))
            return
        print(('uninstalling %s' % self.name))
        self.formula.uninstall()
        self.formula.manifest.status = 'uninstalled'
        self.formula.manifest.delete()

    def clean(self):
        self.formula.clean()

    def test(self):
        print(('testing %s' % self.name))
        self.formula.text()

class Formula:
    """
    A formula describes all the steps that must be taken to build the package.
    The package is downloaded from the URL given in the subclass body to the
    WinBrew cache dir, and then extracted, built, and installed to the WinBrew
    header/library directories.
    """
    def __init__(self):
        self.name = self.__class__.__name__.lower()
        self.work_dir = os.path.abspath(os.path.join(winbrew.cache_path, self.name))
        self.archive = Archive.create(self.url, self.work_dir, self.name)
        self.manifest = Manifest(self.name)
        self.manifest.load()
        try:
            self.options
        except AttributeError:
            self.options = {}

    def parse_options(self, args):
        """
        Parse formula options.
        """
        parser = argparse.ArgumentParser(prog=self.name)
        for name, desc in list(self.options.items()):
            parser.add_argument('--%s' % name, nargs='?', const=True, default=False, help=desc)
        parser.add_argument('remainder', nargs=argparse.REMAINDER)
        self.selected_options = parser.parse_args(args)
        return self.selected_options.remainder

    def option(self, name):
        """
        Returns the value of the selected option, as set by the user.  If the
        option is not set, then return the default value.
        """
        return getattr(self.selected_options, name.replace('-', '_'))

    def build(self):
        """
        Builds the package.
        """
        pass

    def install(self):
        """
        Installs the package.
        """
        pass

    def test(self):
        """
        Tests the package.
        """
        pass

    def patch(self):
        """
        Apply patches for the package.
        """
        pass

    def download(self):
        """
        Download from the source URL via HTTP or git
        """
        self.archive.download()

    def uninstall(self):
        """
        Uninstalls the package.
        """
        for fn in self.manifest.files:
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

    def setenv(self):
        """
        Prepare the package for installation.
        """
        os.environ.clear()
        os.environ.update(winbrew.env)
        os.environ.update({
            'INCLUDE': os.pathsep.join((
                winbrew.env['INCLUDE'],
                winbrew.sdk_include_path,
                winbrew.include_path,
            )),
            'LIBPATH': os.pathsep.join((
                winbrew.env['LIBPATH'],
                winbrew.sdk_lib_path,
                winbrew.lib_path)),
            'LIB': os.pathsep.join((
                winbrew.env['LIB'],
                winbrew.sdk_lib_path,
                winbrew.lib_path,
            )),
            'PATH': os.pathsep.join((
                winbrew.env['PATH'],
                winbrew.sdk_bin_path,
                winbrew.bin_path
            )),
        })

        os.chdir(self.work_dir)

        try:
            os.chdir(self.archive.unpack_dir)
        except OSError as e:
            pass # Unpack name was not a directory

    def verify(self):
        """
        Check the downloaded package against the hash
        """
        sha1 = hashlib.sha1()
        os.chdir(self.work_dir)
        if os.path.isfile(self.archive.name):
            self.sha1_update_for_file(sha1, self.archive.name)
        elif os.path.isdir(self.archive.name):
            for subdir, dirs, files in os.walk(self.archive.name):
                files = [f for f in files if not f[0] == '.']
                dirs[:] = [d for d in dirs if not d[0] == '.']
                for file in files:
                    self.sha1_update_for_file(sha1, os.path.join(subdir, file))
        else:
            raise FormulaException("can't verify package %s: downloaded file not found" % self.name)

        if self.sha1 != sha1.hexdigest():
            raise FormulaException("can't verify package %s: hash doesn't match: %s" % (self.name, sha1.hexdigest()))

    def sha1_update_for_file(self, sha1, filename):
        """
        Verify one file
        """
        fd = open(filename, 'rb')
        chunk_size = 8192
        while True:
            data = fd.read(chunk_size)
            if not data:
                break
            sha1.update(data)

    def clean(self):
        """
        Clean old files from previous builds
        """
        winbrew.util.rm_rf(self.work_dir)

    def unpack(self):
        """
        Extract the project from its zip/tar file if necessary
        """
        self.archive.unpack()

    def cd(self, path):
        """
        Change directories.  Generally used by formulas in the install() method
        """
        os.chdir(path)

    def apply_patch(self, diff):
        """
        Apply patch data from 'diff' to the file at 'path'. 'diff' must
        contain unified diff data.
        """
        #patch.setdebug() broken for python 3
        patcher = patch.fromstring(bytes(diff, 'utf-8'))
        if not patcher:
            self.error("couldn't parse patch")
        if not patcher.apply():
            self.error("couldn't apply patch")

    def system(self, cmd, shell=False, env=os.environ):
        """
        Run a build command.  Used by formulas in the install() method
        """
        subprocess.check_call(shlex.split(cmd), shell=shell, env=env)

    def nmake(self, args=(), env=os.environ):
        """
        Run nmake.  Optionally, the caller can set the arguments to pass to nmake.
        """
        subprocess.check_call(('nmake',)+args, env=env)

    def make(self, args=(), env=os.environ):
        """
        Run make.  Optionally, the caller can set the arguments to pass to nmake.
        """
        subprocess.check_call(('make',)+args, env=env)

    def cmake(self, args=cmake_args, env=os.environ):
        """
        Run cmake.  Optionally, the caller can set arguments to pass to cmake.
        """
        subprocess.check_call(('cmake',)+args, env=env)

    def cmake_build(self, workdir, args=cmake_args):
        """
        Run cmake with the --build option, and build static & shared libs
        """
        env = os.environ.copy()
        env.update({ 'UseEnv': 'true' })

        srcdir = os.getcwd()

        self.mkdir(workdir)
        self.cd(workdir)
        self.cmake(args+(srcdir,))
        self.cmake(('--build', '.', '--config', 'Release'), env=env)
        self.cd(srcdir)

    def scons(self, args=()):
        """
        Run scons.  Optionally, the caller can set arguments to pass to scons.
        """
        subprocess.check_call(('scons',)+args, shell=True)

    def msbuild(self, args=msbuild_args):
        """
        Run msbuild.  Optionally, the caller can set arguments to pass to msbuild.
        """
        subprocess.check_call(('msbuild',)+args)

    def libs(self, path):
        """
        Specify a folder containing library files (DLLs and static libraries).
        All library files in the folder are copied to the winbrew library folder.
        """
        if path[-1] != '\\':
            path += '\\'
        for root, dirs, files in os.walk(path):
            td = os.path.join(winbrew.lib_path, root.replace(path, ''))
            if not os.path.exists(td):
                os.makedirs(td)
            for fn in files:
                lib_files = ('.pdb', '.dll', '.lib', '.exp')
                if os.path.splitext(fn)[1] in lib_files:
                    tf = os.path.join(td, fn)
                    shutil.copyfile(os.path.join(root, fn), tf)
                    self.manifest.files.append(tf)

    def lib(self, path, dest=''):
        """
        Specify a library file to be installed.
        """
        td = os.path.join(winbrew.lib_path, os.path.dirname(dest))
        if not os.path.exists(td):
            os.makedirs(td)
        if dest:
            tf = os.path.join(td, os.path.basename(dest))
        else:
            tf = os.path.join(td, os.path.split(path)[-1])
        shutil.copyfile(path, tf)
        self.manifest.files.append(tf)

    def includes(self, path, dest=''):
        """
        Specify a folder containing C or C++ header files.  All header files in
        the folder are copied to the winbrew library folder.
        """
        if path[-1] != '\\':
            path += '\\'
        for root, dirs, files in os.walk(path):
            td = os.path.join(winbrew.include_path, dest, root.replace(path, ''))
            for fn in files:
                header_files = ('.h', '.hpp', '.hh', '.inl')
                if os.path.splitext(fn)[1] in header_files:
                    if not os.path.exists(td):
                        os.makedirs(td)
                    tf = os.path.join(td, fn)
                    shutil.copyfile(os.path.join(root, fn), tf)
                    self.manifest.files.append(tf)

    def include(self, path, dest=''):
        """
        Specify a single header file.  The file is copied to the winbrew include
        folder.
        """
        td = os.path.join(winbrew.include_path, os.path.dirname(dest))
        if not os.path.exists(td):
            os.makedirs(td)
        if dest:
            tf = os.path.join(td, os.path.basename(dest))
        else:
            tf = os.path.join(td, os.path.split(path)[-1])
        shutil.copyfile(path, tf)
        self.manifest.files.append(tf)

    def bin(self, path, dest=''):
        """
        Specify a single binary executable.  The file is copied to the winbrew
        binaries folder.
        """
        td = os.path.join(winbrew.bin_path, os.path.dirname(dest))
        if not os.path.exists(td):
            os.makedirs(td)
        if dest:
            tf = os.path.join(td, os.path.basename(dest))
        else:
            tf = os.path.join(td, os.path.split(path)[-1])
        shutil.copyfile(path, tf)
        self.manifest.files.append(tf)

    def bins(self, path):
        """
        Specify a folder containing binary files (DLLs and executables libraries).
        All binary files in the folder are copied to the winbrew binary folder.
        """
        if path[-1] != '\\':
            path += '\\'
        for root, dirs, files in os.walk(path):
            td = os.path.join(winbrew.bin_path, root.replace(path, ''))
            if not os.path.exists(td):
                os.makedirs(td)
            for fn in files:
                bin_files = ('.exe', '.dll')
                if os.path.splitext(fn)[1] in bin_files:
                    tf = os.path.join(td, fn)
                    shutil.copyfile(os.path.join(root, fn), tf)
                    self.manifest.files.append(tf)

    def mkdir(self, path):
        winbrew.util.mkdir_p(path)

    def copy(self, path, dest):
        """
        Copies files found at 'path' to a subfolder of winbrew.home
        """
        for root, dirs, files in os.walk(path):
            prefix = re.sub('^'+path.replace('\\', '\\\\')+'\\\\?', '', root)
            td = os.path.join(winbrew.home, dest, prefix)
            for fn in files:
                if not os.path.exists(td):
                    os.makedirs(td)
                tf = os.path.join(td, fn)
                shutil.copyfile(os.path.join(root, fn), tf)
                self.manifest.files.append(tf)

    def error(self, msg):
        """
        Indicates that there was an error while building the package.
        """
        sys.stderr.write('error: %s: %s' % (self.name, msg))
        sys.stderr.flush()
        sys.exit(1)

    @staticmethod
    def find_by_name(name):
        """
        Finds the formula class for the given formula name.  Throws an exception
        if the formula doesn't exist.  Looks for a module in the formula dir first;
        if the module isn't found there, falls back to the default installation.
        """
        try:
            full_name = 'winbrew.formula.%s' % name
            path = os.path.join(winbrew.formula_path, '%s.py' % name)
            module = imp.load_source(full_name, path)
        except IOError as e:
            raise FormulaException('formula "%s" not found' % name)
        return FormulaProxy(getattr(module, name.title())())


