import winbrew
import os

class Cmake(winbrew.Formula):
    url = 'https://github.com/Kitware/CMake/releases/download/v3.15.0-rc2/cmake-3.15.0-rc2-win64-x64.zip'
    homepage = 'http://www.cmake.org'
    sha1 = '55cd33f0f3337c90f7550139c76ce72f49fd8304'
    build_deps = ()
    deps = ()

    def install(self):
        self.bin('bin\\cmake.exe')
        self.copy('share', 'share')

    def test(self):
        self.system('cmake --version')
