
import winbrew

class Libpng(winbrew.Formula):
    url = 'http://prdownloads.sourceforge.net/libpng/lpng1621.zip'
    homepage = 'http://www.libpng.org/pub/png/libpng.html'
    sha1 = '7648d75ce025bb7f2febb7547b637b523c6ef3c0'
    build_deps = ('zlib','cmake')
    deps = ('zlib',)

    def build(self):
        self.cmake_build('build')

    def install(self):
        self.lib('build\\Release\\libpng16.dll','libpng.dll')
        self.lib('build\\Release\\libpng16.lib','libpng.lib')
        self.lib('build\\Release\\libpng16_static.lib','libpng-static.lib')
        self.include('png.h')
        self.include('pngconf.h')
        self.include('pngstruct.h')
        self.include('pnginfo.h')
        self.include('pngdebug.h')
        self.include('build\\pnglibconf.h')

    def test(self):
        pass
