import winbrew

class Nodejs(winbrew.Formula):
    url = 'https://nodejs.org/dist/v6.11.1/node-v6.11.1.tar.gz'
    homepage = 'https://nodejs.org'
    sha1 = '6292aa058ec003e7633e56e714755f2a0e48eb9c'
    build_deps = ()
    deps = ()
    options = {}

    def install(self):
        self.system('vcbuild.bat x64')
        self.bin('Release\\node.exe')
        self.bin('deps\\npm\\bin\\npm')
        self.bin('deps\\npm\\bin\\npm.cmd')
        self.cd('deps')
        self.copy('npm', 'bin\\node_modules\\npm')

    def test(self):
        self.system('node -v')
