
import winbrew

class Fzf(winbrew.Formula):
    url = 'https://github.com/junegunn/fzf/releases/download/0.30.0/fzf-0.30.0-windows_amd64.zip'
    homepage = 'https://github.com/junegunn/fzf'
    sha1 = '9fe3404c8a3743af0a77d7bf1f201867bfe17f30'
    build_deps = ()
    deps = ()

    def build(self):
        self.bin('fzf.exe')

    def install(self):
        pass

    def test(self):
        pass
