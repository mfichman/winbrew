import winbrew
import os

class Freetype2(winbrew.Formula):
    url = 'http://downloads.sourceforge.net/project/freetype/freetype2/2.5.2/freetype-2.5.2.tar.bz2'
    homepage = 'http://freetype.org'
    sha1 = '72731cf405b9f7c0b56d144130a8daafa262b729'
    build_deps = ('cmake',)
    deps = ()

    def install(self):
        self.cmake_build('build', winbrew.cmake_args+(
            '-DCMAKE_CXX_FLAGS=-D_CRT_SECURE_NO_WARNINGS',
            '-DBUILD_SHARED_LIBS=OFF',
        ))
        self.lib('build\\Release\\freetype.lib')
        self.includes('include')

    def test(self):
        pass
