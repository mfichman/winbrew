
import winbrew

class Nasm(winbrew.Formula):
    url = 'http://www.nasm.us/pub/nasm/releasebuilds/2.11.05/win32/nasm-2.11.05-win32.zip'
    homepage = 'http://www.nasm.us/'
    sha1 = '65713cfa2e1913d9c05c05219c605a8108b75069'
    build_deps = ()
    deps = ()

    def install(self):
        self.bin('nasm.exe')
        self.bin('ndisasm.exe')

    def test(self):
        self.system('nasm -v')
