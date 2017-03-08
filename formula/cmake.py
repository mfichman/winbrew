import winbrew
import os

class Cmake(winbrew.Formula):
    url = 'https://cmake.org/files/v3.7/cmake-3.7.2-win32-x86.zip'
    homepage = 'http://www.cmake.org'
    sha1 = 'c80c17e858ecfebfaf16fe8af18b174d2600c4e6'
    build_deps = ()
    deps = ()

    def install(self):
        self.bin('bin\\cmake.exe')
        self.copy('share', 'share')

    def test(self):
        self.system('cmake --version')
