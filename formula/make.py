
import winbrew
import shutil

class Make(winbrew.Formula):
    url = 'http://gnu.mirrors.pair.com/make/make-4.2.tar.gz'
    homepage = 'http://gnuwin32.sourceforge.net/packages/make.htm'
    sha1 = '0ae8f44ad73e66d8f7b91e7e2e39ed8a8f2c7428'
    build_deps = ()
    deps = ()

    def install(self):
        shutil.copy('config.h.W32','config.h')
        self.system('build_w32.bat')
        self.bin('WinRel\\gnumake.exe', 'make.exe')

    def test(self):
        pass
