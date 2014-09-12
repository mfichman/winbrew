
import winbrew

class Scons(winbrew.Formula):
    url = 'https://downloads.sourceforge.net/scons/scons-2.3.0.tar.gz'
    homepage = 'http://www.scons.org'
    sha1 = '7a5883fcc41af47e7ecd71096c19371788d9eb20'
    build_deps = ()
    deps = ()

    def install(self):
        self.system('python setup.py install')

    def test(self):
        self.system('scons -v')
