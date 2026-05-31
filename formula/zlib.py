
import winbrew

class Zlib(winbrew.Formula):
    url = 'https://zlib.net/fossils/zlib-1.3.1.tar.gz'
    homepage = 'http://www.zlib.net/'
    sha1 = 'f535367b1a11e2f9ac3bec723fb007fbc0d189e5'
    build_deps = ('cmake',)
    deps = ()

    def build(self):
        self.cmake_build('build')
        self.lib('build\\Release\\zlib.dll')
        self.lib('build\\Release\\zlib.lib')
        self.lib('build\\Release\\zlibstatic.lib','zlib-static.lib')

    def install(self):
        self.include('zlib.h')
        self.include('zutil.h')
        self.include('build\\zconf.h')

    def test(self):
        pass
