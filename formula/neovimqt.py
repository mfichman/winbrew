
import winbrew

class Neovimqt(winbrew.Formula):
    url = 'https://github.com/equalsraf/neovim-qt/releases/download/v0.2.16.1/neovim-qt.zip'
    homepage = 'https://github.com/equalsraf/neovim-qt'
    sha1 = '8544c5dd53d6b0443dc9ac183ae622e27c19892a'
    build_deps = ()
    deps = ()

    def build(self):
        pass

    def install(self):
        self.bin('bin//nvim-qt.exe')
        self.bins('bin')

    def test(self):
        pass
