import winbrew
class Jpeg(winbrew.Formula):
    url = 'https://github.com/libjpeg-turbo/libjpeg-turbo/archive/refs/tags/3.1.2.zip'
    homepage = 'https://libjpeg-turbo.org'
    sha1 = '5b55aba04b63536195bd4b1f5ee3742e0e665dad'
    build_deps = ('cmake',)
    deps = ()

    def build(self):
        self.cmake_build('build', winbrew.cmake_args+(
            '-DENABLE_SHARED=OFF',
            '-DWITH_TURBOJPEG=OFF',
        ))

    def install(self):
        self.lib('build\\Release\\jpeg-static.lib', 'jpeg.lib')
        self.include('build\\jconfig.h')
        self.include('src\\jerror.h')
        self.include('src\\jmorecfg.h')
        self.include('src\\jpeglib.h')

    def test(self):
        pass
