import winbrew
import os

class Cmake(winbrew.Formula):
    url = 'http://www.cmake.org/files/v2.8/cmake-2.8.12-win32-x86.zip'
    homepage = 'http://www.cmake.org'
    sha1 = '1802fd2bedb3ef2b7962b9ca48ca53edb0451af0'
    build_deps = ()
    deps = ()

    def install(self):
        self.cd('bin')
        self.bin('cmake.exe')
        self.bin('cmake-gui.exe')
        self.bin('cpack.exe')
        self.bin('ctest.exe')
        self.bin('cmcldeps.exe')
        self.bin('cmw9xcom.exe')
        self.libs('.')
        self.cd('..')
        self.copy('share')

    def test(self):
        self.system('cmake --version')
