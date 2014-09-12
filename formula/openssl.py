import winbrew

class Openssl(winbrew.Formula):
    url = 'http://www.openssl.org/source/openssl-1.0.1g.tar.gz'
    homepage = 'http://www.openssl.org'
    sha1 = '95c1c4e7f4164efaa14be5edbd5a21ca64073dc3'
    build_deps = ('perl',)
    deps = ()

    def install(self):
        self.system('perl Configure VC-WIN32 no-asm --prefix=C:\\Winbrew\\lib\\OpenSSL')
        self.system('ms\\\\do_ms.bat')
        self.system('nmake -f ms\\\\nt.mak')
        self.lib('out32\\libeay32.lib')
        self.lib('out32\\ssleay32.lib')
        self.includes('include\\openssl', dest='openssl')
        #self.system('nmake -f ms\\ntdll.mak install')
        # Dynamic libraries

    def test(self):
        self.system('nmake -f ms\\\\nt.mak test')
