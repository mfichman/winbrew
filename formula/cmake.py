import winbrew
import os

class Cmake(winbrew.Formula):
    url = 'https://github.com/Kitware/CMake/releases/download/v4.1.0/cmake-4.1.0-windows-x86_64.zip'
    homepage = 'http://www.cmake.org'
    sha1 = '0145b3b0ea046f6e1da2e374965955cc29b7b162'
    build_deps = ()
    deps = ()

    def install(self):
        self.bin('bin\\cmake.exe')
        self.copy('share', 'share')

    def test(self):
        self.system('cmake --version')
