import winbrew
import os

class Openssl(winbrew.Formula):
    url = 'http://openssl.org/source/openssl-1.0.2e.tar.gz'
    homepage = 'http://www.openssl.org'
    sha1 = '2c5691496761cb18f98476eefa4d35c835448fb6'
    build_deps = ('perl',)
    deps = ()

    def build(self):
        os.environ['PATH'] = ';'.join((os.environ['PATH'], os.path.join(winbrew.cache_path, 'perl\\perl\\bin')))
        self.system(r'perl Configure no-asm VC-WIN64A --prefix=%s' % os.path.join(winbrew.cache_path, 'openssl').replace('\\','\\\\'))
        self.system(r'call ms\\do_win64a.bat', shell=True)
        self.system(r'nmake -f ms\\nt.mak')

    def install(self):
        self.lib(r'out32\libeay32.lib','libeay.lib')
        self.lib(r'out32\ssleay32.lib','ssleay.lib')
        self.includes(r'inc32\openssl', dest='openssl')
        #self.system('nmake -f ms\\ntdll.mak install')
        # Dynamic libraries

    def test(self):
        self.system(r'nmake -f ms\\nt.mak test')
