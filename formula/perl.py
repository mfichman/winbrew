import winbrew

class Perl(winbrew.Formula):
    url = 'http://downloads.activestate.com/ActivePerl/releases/5.16.3.1603/ActivePerl-5.16.3.1603-MSWin32-x86-296746.msi'
    homepage = 'http://activestate.com'
    sha1 = '0c947ec21b2a76233a7f821fcb46b6e494b189df'
    build_deps = ()
    deps = ()

    def install(self):
        self.system('perl -v')
