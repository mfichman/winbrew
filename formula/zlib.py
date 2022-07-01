
import winbrew

class Zlib(winbrew.Formula):
    url = 'https://zlib.net/zlib-1.2.11.tar.gz'
    homepage = 'http://www.zlib.net/'
    sha1 = 'e6d119755acdf9104d7ba236b1242696940ed6dd'
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
