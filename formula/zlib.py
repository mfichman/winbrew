
import winbrew

class Zlib(winbrew.Formula):
    url = 'http://zlib.net/zlib-1.2.8.tar.gz'
    homepage = 'http://www.zlib.net/'
    sha1 = 'a4d316c404ff54ca545ea71a27af7dbc29817088'
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
