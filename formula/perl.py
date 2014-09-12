import winbrew

class Perl(winbrew.Formula):
    url = 'http://downloads.activestate.com/ActivePerl/releases/5.16.3.1603/ActivePerl-5.16.3.1603-MSWin32-x86-296746.msi'
    homepage = 'http://activestate.com'
    sha1 = '7a6da13387b9e6472d73c7251c599462dfd9e92d'
    build_deps = ()
    deps = ()

    def install(self):
        self.system('perl -v')
