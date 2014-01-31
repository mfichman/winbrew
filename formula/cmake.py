import winbrew
import os

class Cmake(winbrew.Formula):
    url = 'http://www.cmake.org/files/v2.8/cmake-2.8.12-win32-x86.zip'
    homepage = 'http://www.cmake.org'
    sha1 = ''
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
        self.cd('..')
        self.copy('share')

    def test(self):
        pass
