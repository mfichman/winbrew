
import winbrew

class Libpng(winbrew.Formula):
    url = 'https://netactuate.dl.sourceforge.net/project/libpng/libpng16/1.6.37/lpng1637.zip'
    homepage = 'http://www.libpng.org/pub/png/libpng.html'
    sha1 = 'a3fe518a427981c34f2eca964a73ab04e10e3309'
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
