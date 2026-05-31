import winbrew
import os

class Cmake(winbrew.Formula):
    url = 'https://github.com/Kitware/CMake/releases/download/v4.3.3/cmake-4.3.3-windows-x86_64.zip'
    homepage = 'http://www.cmake.org'
    sha1 = '3e3f0adf3e1bea5d1d0b783b3a9c3d22428f96b4'
    build_deps = ()
    deps = ()

    def install(self):
        self.bin('bin\\cmake.exe')
        self.copy('share', 'share')

    def test(self):
        self.system('cmake --version')
