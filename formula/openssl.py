import winbrew
import os

class Openssl(winbrew.Formula):
    url = 'http://openssl.org/source/openssl-1.0.2e.tar.gz'
    homepage = 'http://www.openssl.org'
    sha1 = '2c5691496761cb18f98476eefa4d35c835448fb6'
    build_deps = ('perl',)
    deps = ()

    def install(self):
        os.environ['PATH'] = ';'.join((os.environ['PATH'], os.path.join(winbrew.cache_path, 'perl\\perl\\bin')))
        self.system('perl Configure no-asm VC-WIN32 --prefix=%s' % os.path.join(winbrew.cache_path, 'openssl').replace('\\','\\\\'))
        self.system('ms\\\\do_ms.bat')
        self.system('nmake -f ms\\\\nt.mak')
        self.lib('out32\\libeay32.lib')
        self.lib('out32\\ssleay32.lib')
        self.includes('include\\openssl', dest='openssl')
        #self.system('nmake -f ms\\ntdll.mak install')
        # Dynamic libraries

    def test(self):
        self.system('nmake -f ms\\\\nt.mak test')
