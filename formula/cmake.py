import winbrew
import os

class Cmake(winbrew.Formula):
    url = 'https://github.com/Kitware/CMake/releases/download/v3.22.0-rc2/cmake-3.22.0-rc2-windows-x86_64.zip'
    homepage = 'http://www.cmake.org'
    sha1 = 'a247db660b0b4899ea8e66f6560dbde9741225be'
    build_deps = ()
    deps = ()

    def install(self):
        self.bin('bin\\cmake.exe')
        self.copy('share', 'share')

    def test(self):
        self.system('cmake --version')
