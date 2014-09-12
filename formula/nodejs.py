import winbrew

class Nodejs(winbrew.Formula):
    url = 'http://nodejs.org/dist/v0.10.29/node-v0.10.29.tar.gz'
    homepage = 'https://nodejs.org'
    sha1 = 'a9de5816a07ec697bda92e1a7694ed03de44e3b4'
    build_deps = ()
    deps = ()
    options = {}

    def install(self):
        self.system('vcbuild.bat')
        self.bin('Release\\node.exe')
        self.bin('deps\\npm\\bin\\npm')
        self.bin('deps\\npm\\bin\\npm.cmd')
        self.cd('deps')
        self.copy('npm', 'bin\\node_modules')

    def test(self):
        self.system('node -v')
