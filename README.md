Winbrew
=======

A Homebrew-inspired package manager for Windows.

Why Winbrew?
------------

Windows has a tricky ecosystem when it comes to building and packaging native (C/C++) software. Unlike Unix developers,
who have mostly settled on Autotools (`./configure`, `make install`) Windows developers use many
build systems: CMake, Boost jam, SCons, plain ol' msbuild, NMake, etc. This plethora of build systems makes finding/building dependencies for a particular Visual Studio runtime version a real pain. 

Other Windows package managers distribute software that's packaged for `msiexec` (or similar). These package managers aren't designed for developers, and don't really follow the "Homebrew spirit":

* Don't duplicate what the system gives
* Use the default system compilers
* Build from source
* Formulae are simple scripts

Winbrew provides all of the above for Windows development work.


Installing Winbrew
------------------

Download and install [Microsoft Visual Studio](http://www.visualstudio.com/), then install Winbrew using `pip`:

    pip install winbrew    

To use files installed by Winbrew in your builds, set these environment variables:

    set PATH=%PATH%;C:\WinBrew\lib;C:\WinBrew\bin
    set LIB=%LIB%;C:\WinBrew\lib
    set INCLUDE=%INCLUDE%;C:\WinBrew\include


Basic usage
-----------

    winbrew install <package>
    
Winbrew installs all packages to C:\Winbrew by default, but you can change this by setting `WINBREW_HOME`.


Want to contribute?
-------------------

Winbrew needs authors to help write additional formulae! For more info, read [CONTRIBUTING.md](https://github.com/mfichman/winbrew/blob/master/CONTRIBUTING.md).

