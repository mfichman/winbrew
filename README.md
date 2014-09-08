Winbrew
=======

A homebrew-inspired package manager for Windows.


Installing Winbrew
------------------

Install Winbrew using `pip`:

    pip install winbrew    

Then, add these directories to your PATH environment variable:

    C:\WinBrew\lib
    C:\WinBrew\bin


Basic Usage
-----------

    winbrew install sfml

That's it!


Creating a new formula
----------------------

To create a new formula, run `winbrew create`:

    winbrew create NewPkg

This opens a text editor with the new formula. An empty formula looks like this:

    import winbrew

    class NewPkg(winbrew.Formula):
        url = ''
        homepage = ''
        sha1 = ''
        build_deps = ()
        deps = ()

        def install(self):
            pass

        def test(self):
            pass 

At minimum, you should fill in the `url`, `homepage`, `sha1`, and `deps` attributes:
* `url` is the download URL for the package.
* `homepage` is a link to the package's homepage.
* `sha1` is the SHA-1 hash of the downloaded package.
* `deps` is a list of dependencies that WinBrew installs before the package is installed.
* `build_deps` is a list of dependencies that WinBrew installs when building
  your package. Be sure to include build systems, like `cmake` here!

## Configuring the build

In `install`, you need to insert code to build the package and install
libraries, headers, executables, etc. Windows packages have a wide variety of
build systems; you need to select the build system the new package uses.
WinBrew has support for a few build systems built-in. **Note that all build
commands are run in the root directory of the unpacked source zip/tar.** Here
are some examples:

### msbuild

    def install(self):
        self.msbuild(winbrew.msbuild_args+('NewPackage.vcxproj'))

### cmake+msbuild

    def install(self):
        self.cmake(('-G', 'Visual Studio 12', '-DCMAKE_BUILD_TYPE=Release'))
        self.msbuild(winbrew.msbuild_args+('NewPackage.vcxproj'))

### scons

    def install(self):
        self.scons()

### nmake
    
    def install(self):
        self.nmake()

### other

If the build system is not supported, you can use `system` to execute an arbitrary build command:

    def install(self):
        self.system('NewPackageBuild.bat')

## Build output

When creating a new package, you need to indicate what build output (headers,
libraries, exeutables) WinBrew should install. This is done with the `libs`,
`includes`, and `bin` commands:

    def install(self):
        # Build commands here
        ...

        # Install all .lib and .dll files from "Release" to %WINBREW_HOME%\lib
        self.libs('Release') 

        # Install a single lib
        self.lib('Release\\foo.lib')
    
        # Install all headers (.h, .hpp) from "Include" to %WINBREW_HOME%\include
        self.includes('Include') 

        # Install a single header
        self.include('NewPkg.h')
        
        # Install an executable to %WINBREW_HOME%\bin
        self.bin('Bin\\NewPackage.exe') 

        # Copy all data files to $WINBREW_HOME%\Path\To\Data
        self.copy('Path\\To\\Data') 

## Tests

The `test` function should run a short sanity test to insure the package was
installed correctly.  For packages with an executable, running the executable
with the `--version` option (or similar) is sufficient.

    def test(self):
        self.system('NewPkg.exe --version')

## Full working example

Here's an example for the SFML package:

    class Sfml(winbrew.Formula):
        url = 'https://github.com/LaurentGomila/SFML/archive/2.1.zip'
        homepage = 'http://sfml-dev.org'
        sha1 = 'ff345985a301bbee350b1193f48f712acc656fc6'
        build_deps = ('cmake',)
        deps = ()
            
        options = {
            'build-examples': 'Build example programs',
            'debug': 'Build debug libraries',
        }           
                        
        def install(self):
            self.cmake(('-G', 'Visual Studio 12',
                '-DSFML_BUILD_EXAMPLES=%s' % ('ON' if self.option('build-examples') else 'OFF'),
                #'-DSFML_USE_STATIC_STD_LIBS=%s' % ('OFF' if self.option('shared') else 'ON'),
            ))
            config = '/p:Configuration=%s' % ('Debug' if self.option('debug') else 'Release')
            self.msbuild(winbrew.msbuild_args+('SFML.sln',config))
            self.libs('lib\\%s' % ('Debug' if self.option('debug') else 'Release'))
            self.includes('include') 
            
        def test(self):
            pass 

