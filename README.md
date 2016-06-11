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

Dependencies
------------
* **Python** 2.x (and **pip** on PATH)
* [Microsoft Visual Studio 2015](http://www.visualstudio.com/)
* **GIT** 2.x or newer
* **64-bit** platform

Installing Winbrew
------------------

Install Winbrew using `pip`:

```sh
pip install winbrew    
```

To use files installed by Winbrew in your builds, set these environment variables:

```sh
set PATH=%PATH%;%LOCALAPPDATA%\WinBrew\lib;%LOCALAPPDATA%\WinBrew\bin
set LIB=%LIB%;%LOCALAPPDATA%\WinBrew\lib
set INCLUDE=%INCLUDE%;%LOCALAPPDATA%\WinBrew\include
```

Basic usage
-----------

Open the Visual Studio 2015 Cross Tools command prompt, then type:

```sh
winbrew install <package>
```

or

```sh
brew install <package>
```

Winbrew installs all packages to `%LOCALAPPDATA%` by default, but you can
change this by setting `%WINBREW_HOME%`. Also, note that WinBrew always
builds 64-bit binaries.


Want to contribute?
-------------------

Winbrew needs authors to help write additional formulae! For more info, read
[CONTRIBUTING.md](https://github.com/mfichman/winbrew/blob/master/CONTRIBUTING.md).

