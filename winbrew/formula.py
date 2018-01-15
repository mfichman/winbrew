import subprocess
import sys
import os
import zipfile
import tarfile
import urllib
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

# Default arguments for the supported build tools
cmake_args = ('-G', 'Visual Studio 15 2017 Win64', '--build', 'build64')
msbuild_args = ('/P:Configuration=Release', '/p:PlatformToolset=v141', '/p:UseEnv=true')

class FormulaException(Exception):
    pass

class Formula:
    """
    A formula describes all the steps that must be taken to build the package.
    The package is downloaded from the URL given in the subclass body to the
    WinBrew cache dir, and then extracted, built, and installed to the WinBrew
    header/library directories.
    """
    def __init__(self):
        self.archive_name = os.path.split(self.url)[1]
        self.ext = os.path.splitext(self.archive_name)[1]
        self.name = self.__class__.__name__.lower()
        self.workdir = os.path.abspath(os.path.join(winbrew.cache_path, self.name))
        self.manifest = Manifest(self.name)
        try:
            self.options
        except AttributeError:
            self.options = {}

    def parse_options(self, args):
        """
        Parse formula options.
        """
        parser = argparse.ArgumentParser(prog=self.name)
        for name, desc in self.options.iteritems():
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

    def download(self):
        """
        Download from the source URL via HTTP or git
        """
        print('downloading %s' % self.name)
        if self.ext == '.git':
            path = os.path.join(self.workdir, self.name)
            winbrew.util.mkdir_p(self.workdir)
            os.chdir(self.workdir)
            if not os.path.exists(self.name):
                subprocess.check_call(('git', 'clone', self.url, self.name))
                if getattr(self, 'tag'):
                    subprocess.check_call(('git', 'checkout', tab))
            self.unpack_name = self.name
            self.archive_name = self.name
        else:
            path = os.path.join(self.workdir, self.archive_name)
            if not os.path.exists(path):
                winbrew.util.rm_rf(self.workdir)
                winbrew.util.mkdir_p(self.workdir)
                os.chdir(self.workdir)
                stream = urllib.request.urlopen(self.url)
                fd = open(self.archive_name, 'wb')
                shutil.copyfileobj(stream, fd)
                fd.close()

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
        os.chdir(self.workdir)
        if self.ext == 'git':
            subprocess.check_call(('git', '-C', self.archive_name, 'reset', '--hard'))
            subprocess.check_call(('git', '-C', self.archive_name, 'clean', '-dxf'))
        for fn in os.listdir('.'):
            if fn != self.archive_name:
                winbrew.util.rm_rf(fn)

    def verify(self):
        """
        Check the downloaded package against the hash
        """
        sha1 = hashlib.sha1()
        os.chdir(self.workdir)
        if os.path.isfile(self.archive_name):
            self.sha1_update_for_file(sha1, self.archive_name)
        elif os.path.isdir(self.archive_name):
            for subdir, dirs, files in os.walk(self.archive_name):
                files = [f for f in files if not f[0] == '.']
                dirs[:] = [d for d in dirs if not d[0] == '.']
                for file in files:
                    self.sha1_update_for_file(sha1, os.path.join(subdir, file))
        else:
            raise FormulaException("can't verify package %s: downloaded file not found" % self.name)

        if self.sha1 != sha1.hexdigest():
            raise FormulaException("can't verify package %s: hash doesn't match: %s" % (self.name, sha1.hexdigest()))

    def unpack(self):
        """
        Extract the project from its zip/tar file if necessary
        """
        print('unpacking %s' % self.name)
        os.chdir(self.workdir)
        if self.ext == '.zip':
            self.unzip()
        elif self.ext == '.gz':
            self.untar()
        elif self.ext == '.tgz':
            self.untar()
        elif self.ext == '.bz2':
            self.untar(compression='bz2')
        elif self.ext == '.msi':
            self.msi()
        elif self.ext == '.git':
            pass
        else:
            raise Exception('unknown file type')

    def setup(self):
        """
        Prepare the package for installation -- then install it.
        """
        print('installing %s' % self.name)
        os.chdir(self.workdir)
        try:
            os.chdir(self.unpack_name)
        except OSError as e:
            pass # Unpack name was not a directory
        os.environ.update({
            'INCLUDE': ';'.join((
                os.environ['INCLUDE'],
                winbrew.sdk_include_path,
                winbrew.include_path,
            )),
            'LIBPATH': ';'.join((
                os.environ['LIBPATH'],
                winbrew.sdk_lib_path,
                winbrew.lib_path)),
            'LIB': ';'.join((
                os.environ['LIB'],
                winbrew.sdk_lib_path,
                winbrew.lib_path,
            )),
            'PATH': ';'.join((
                os.environ['PATH'],
                winbrew.sdk_bin_path,
                winbrew.bin_path
            )),
        })
        self.install()

    def cd(self, path):
        """
        Change directories.  Generally used by formulas in the install() method
        """
        os.chdir(path)

    def patch(self, diff):
        """
        Apply patch data from 'diff' to the file at 'path'. 'diff' must
        contain unified diff data.
        """
        patch.setdebug()
        patcher = patch.fromstring(diff)
        if not patcher:
            self.error("couldn't apply patch")
        if not patcher.apply():
            self.error("couldn't apply patch")

    def msi(self):
        """
        Install a MSI-style installer
        """
        self.system('msiexec /quiet /i %s' % self.archive_name)
        self.unpack_name = '.'

    def unzip(self):
        """
        Unzip the downloaded zip file into the current working directory
        """
        fd = open(self.archive_name, 'rb')
        zf = zipfile.ZipFile(fd)
        self.unpack_name = os.path.commonprefix(zf.namelist())
        if os.path.exists(self.unpack_name):
            pass # already extracted
        else:
            zf.extractall()

    def untar(self, compression='gz'):
        """
        Extract the downloaded tar file into the current working directory
        """
        tf = tarfile.open(self.archive_name, mode='r:%s' % compression)
        self.unpack_name = os.path.commonprefix(tf.getnames())
        if os.path.exists(self.unpack_name):
            pass
        else:
            tf.extractall()

    def system(self, cmd, shell=False):
        """
        Run a build command.  Used by formulas in the install() method
        """
        subprocess.check_call(shlex.split(cmd), shell=shell)

    def nmake(self, args=(), env=os.environ):
        """
        Run nmake.  Optionally, the caller can set the arguments to pass to nmake.
        """
        subprocess.check_call(('nmake',)+args, env=env)

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
        binaries bolder.
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
    def formula_by_name(name):
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
        return getattr(module, name.title())


