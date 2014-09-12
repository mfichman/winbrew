import winbrew

class Perl(winbrew.Formula):
    url = 'http://downloads.activestate.com/ActivePerl/releases/5.16.3.1603/ActivePerl-5.16.3.1603-MSWin32-x86-296746.msi'
    homepage = 'http://activestate.com'
    sha1 = '332d9292c17e43fc5661e899be729cf0f98b26a6'
    build_deps = ()
    deps = ()

    def install(self):
        self.system('perl -v')
