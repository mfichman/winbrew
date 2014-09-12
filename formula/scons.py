
import winbrew

class Scons(winbrew.Formula):
    url = 'https://downloads.sourceforge.net/scons/scons-2.3.0.tar.gz'
    homepage = 'http://www.scons.org'
    sha1 = '728edf20047a9f8a537107dbff8d8f803fd2d5e3'
    build_deps = ()
    deps = ()

    def install(self):
        self.system('python setup.py install')

    def test(self):
        self.system('scons -v')
