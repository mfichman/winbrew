Winbrew
=======

A Homebrew-inspired package manager for Windows.

Why Winbrew?
------------

Windows has a tricky ecosystem when it comes to building and packaging native
(C/C++) software. Unlike Unix developers, who have mostly settled on Autotools
(`./configure`, `make install`) Windows developers use many build systems:
CMake, Boost jam, SCons, plain ol' msbuild, NMake, etc. This plethora of build
systems makes finding/building dependencies for the latest Visual Studio
runtime version a real pain.

Other Windows package managers distribute software that's packaged for
`msiexec` (or similar). These package managers aren't designed for developers,
and don't really follow the "Homebrew spirit":

* Don't duplicate what the system provides already
* Use the default system compilers
* Build from source
* Formulae are simple scripts

Winbrew provides all of the above for Windows development work.


Installing Winbrew
------------------

Download and install [Microsoft Visual Studio
2017](http://www.visualstudio.com/), then install Winbrew using `pip`:

    pip install winbrew

To use files installed by Winbrew in your builds, set these environment variables:

    set PATH=%PATH%;%LOCALAPPDATA%\WinBrew\lib;%LOCALAPPDATA%\WinBrew\bin
    set LIB=%LIB%;%LOCALAPPDATA%\WinBrew\lib
    set INCLUDE=%INCLUDE%;%LOCALAPPDATA%\WinBrew\include


Basic usage
-----------

Open the Visual Studio 2017 x86 x64 Cross Tools command prompt, then type:

    winbrew install <package>

Winbrew installs all packages to `%LOCALAPPDATA%\WinBrew` by default, but you can
change this by setting `%WINBREW_HOME%`. Also, note that WinBrew always
builds 64-bit binaries.


Visual Studio version support
-----------------------------

Winbrew supports 64-bit builds using the latest Visual Studio version, which is
currently Visual Studio 2017.

Winbrew may work with 32-bit builds and older Visual Studio versions with minor
tweaks to individual formulas. However, keep in mind that 32-bit builds and
older Visual Studio versions aren't officially supported.

Want to contribute?
-------------------

Winbrew needs authors to help write additional formulae! For more info, read
[CONTRIBUTING.md](https://github.com/mfichman/winbrew/blob/master/CONTRIBUTING.md).

