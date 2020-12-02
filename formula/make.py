
import winbrew
import shutil

class Make(winbrew.Formula):
    url = 'http://gnu.mirrors.pair.com/make/make-4.3.tar.gz'
    homepage = 'http://gnuwin32.sourceforge.net/packages/make.htm'
    sha1 = '3c40e5b49b893dbb14f1e2e1f8fe89b7298cc51d'
    build_deps = ()
    deps = ()

    def build(self):
        self.system('build_w32.bat')

    def install(self):
        self.bin('WinRel\\gnumake.exe', 'make.exe')

    def test(self):
        pass
