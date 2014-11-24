import winbrew
import os

class Cmake(winbrew.Formula):
    url = 'http://www.cmake.org/files/v2.8/cmake-2.8.12.2-win32-x86.zip'
    homepage = 'http://www.cmake.org'
    sha1 = '0d778fe630e623c881c14e1fef7b6ad40f68055c'
    build_deps = ()
    deps = ()

    def install(self):
        self.bin('bin\\cmake.exe')
        self.copy('share', 'share')

    def test(self):
        self.system('cmake --version')
