
import winbrew

class Ogg(winbrew.Formula):
    url = 'http://downloads.xiph.org/releases/ogg/libogg-1.3.2.zip'
    homepage = 'http://www.vorbis.com/setup/'
    sha1 = 'd7ce7b73f13a2c6e0e90ad212ffb21ec22ca42e3'
    build_deps = ()
    deps = ()

    def build(self):
        self.msbuild(args=('win32\\VS2010\\libogg_static.sln',)+winbrew.formula.msbuild_args)

    def install(self):
        self.lib('win32\\VS2010\\x64\\Release\\libogg_static.lib', dest='ogg.lib')
        self.includes('include')

    def test(self):
        pass
