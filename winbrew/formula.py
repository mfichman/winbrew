import subprocess
import sys
import os
import zipfile
import tarfile
import urllib2
import errno
import glob
import shutil
import shlex
import imp
import winbrew
import winbrew.formulas
import pickle

# Default arguments for the supported build tools
cmake_args = ('-G', 'NMake Makefiles')
msbuild_args = ('/P:Configuration=Release',)

class Manifest:
    """
    Stores a list of all files installed by a formula.  This class is used to 
    deteremine which files to uninstall, and to check for conflicts between
    formulas.
    """
    def __init__(self, name):
        self.files = []
        self.name = name
        self.path = os.path.join(winbrew.manifest_path, self.name)

    def save(self):
        """
        Write the manifest to the manifest file directory 
        """
        if not os.path.exists(winbrew.manifest_path):
            os.makedirs(winbrew.manifest_path)
        with open(self.path, 'wb') as fd:
            pickle.dump(self.files, fd, pickle.HIGHEST_PROTOCOL)
        
    def load(self):
        """ 
        Read the manifest from the manifest file directory
        """
        with open(self.path, 'rb') as fd:
            self.files = pickle.load(fd) 
        

class Formula:
    """
    A formula describes all the steps that must be taken to build the package.
    The package is downloaded from the URL given in the subclass body to the
    WinBrew cache dir, and then extracted, built, and installed to the WinBrew
    header/library directories.
    """
    def __init__(self):
        self.filename = os.path.split(self.url)[1]
        self.ext = os.path.splitext(self.filename)[1]
        self.name = self.__class__.__name__.lower()
        self.workdir = os.path.join(winbrew.cache_path, self.name)
        self.manifest = Manifest(self.name)

    def download(self):
        """
        Download from the source URL via HTTP or git
        """
        print('downloading %s' % self.name)
        if not os.path.exists(self.workdir):
            os.makedirs(self.workdir)
        os.chdir(self.workdir)
        # FIXME: Git support
        if os.path.exists(self.filename): 
            return # FIXME: Check hash instead
        stream = urllib2.urlopen(self.url)
        fd = open(self.filename, 'wb')
        fd.write(stream.read())
        fd.close()
        self.unpack()

    def unpack(self):
        """
        Extract the project from its zip/tar file if necessary
        """
        os.chdir(self.workdir)
        if self.ext == '.zip':
            self.unzip()
        elif self.ext == '.tar.gz':
            self.untar()
        elif self.ext == '.tgz':
            self.untar()
        else:
            raise Exception('unknown file type')

    def setup(self):
        """
        Prepare the package for installation -- then install it.
        """
        print('installing %s' % self.name)
        os.chdir(self.workdir)
        self.install()

    def cd(self, path):
        """
        Change directories.  Generally used by formulas in the install() method
        """
        os.chdir(path)

    def unzip(self):
        """
        Unzip the downloaded zip file into the current working directory
        """ 
        fd = open(self.filename, 'rb')
        zf = zipfile.ZipFile(fd)
        zf.extractall()

    def untar(self):
        """
        Extract the downloaded tar file into the current working directory
        """
        tf = tarfile.open(self.filename, mode='r:gz')
        tf.extractall()

    def system(self, cmd):
        """
        Run a build command.  Used by formulas in the install() method
        """
        subprocess.check_call(shlex.split(cmd))

    def nmake(self, args=()):
        """
        Run nmake.  Optionally, the caller can set the arguments to pass to nmake.
        """
        subprocess.check_call(('nmake',)+args)

    def cmake(self, cwd='.', args=cmake_args):
        """
        Run cmake.  Optionally, the caller can set arguments to pass to cmake.
        """
        subprocess.check_call(('cmake',)+args)

    def scons(self, cwd='.', args=()):
        """
        Run scons.  Optionally, the caller can set arguments to pass to scons.
        """
        pass

    def msbuild(self, cwd='.', args=msbuild_args):
        """
        Run msbuild.  Optionally, the caller can set arguments to pass to msbuild.
        """
        subprocess.check_call(('msbuild',)+msbuild_args)

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

    def includes(self, path):
        """
        Specify a folder containing C or C++ header files.  All header files in
        the folder are copied to the winbrew library folder.
        """
        if path[-1] != '\\':
            path += '\\'
        for root, dirs, files in os.walk(path):
            td = os.path.join(winbrew.include_path, root.replace(path, ''))
            for fn in files:
                header_files = ('.h', '.hpp', '.hh')
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

    @staticmethod
    def formula_by_name(name):
        """
        Finds the formula class for the given formula name.  Throws an exception 
        if the formula doesn't exist.  Looks for a module in the formula dir first;
        if the module isn't found there, falls back to the default installation.
        """
        try:
            full_name = 'winbrew.formulas.%s' % name
            path = os.path.join(winbrew.formula_path, 'winbrew\\formulas\\%s.py' % name)
            module = imp.load_source(full_name, path)
        except IOError, e:
            try:
                __import__(full_name)
                module = sys.modules[full_name]
            except ImportError, e:
                raise Exception('formula "%s" not found' % name)
        return getattr(module, name.title())

