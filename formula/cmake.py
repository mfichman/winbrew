import winbrew
import os

class Cmake(winbrew.Formula):
    url = 'https://cmake.org/files/v3.4/cmake-3.4.1-win32-x86.zip'
    homepage = 'http://www.cmake.org'
    sha1 = '4894baeafc0368d6530bf2c6bfe4fc94056bd04a'
    build_deps = ()
    deps = ()

    def install(self):
        self.bin('bin\\cmake.exe')
        self.copy('share', 'share')

    def test(self):
        self.system('cmake --version')
