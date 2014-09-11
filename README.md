Winbrew
=======

A homebrew-inspired package manager for Windows.


Installing Winbrew
------------------

Download and install [Microsoft Visual Studio](http://www.visualstudio.com/), then install Winbrew using `pip`:

    pip install winbrew    

To use files installed by Winbrew in your builds, you might want to set these environment variables:

    set PATH=%PATH%;C:\WinBrew\lib;C:\WinBrew\bin
    set LIB=%LIB%;C:\WinBrew\lib
    set INCLUDE=%INCLUDE%;C:\WinBrew\include


Basic usage
-----------

    winbrew install <package>


Want to contribute?
-------------------

Winbrew needs authors to write additional formulae! For more info, read [CONTRIBUTING.md](https://github.com/mfichman/winbrew/blob/master/CONTRIBUTING.md).

