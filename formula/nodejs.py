import winbrew

class Nodejs(winbrew.Formula):
    url = 'http://nodejs.org/dist/v0.10.29/node-v0.10.29.tar.gz'
    homepage = 'https://nodejs.org'
    sha1 = '0d5dc62090404f7c903f29779295758935529242'
    build_deps = ()
    deps = ()
    options = {}

    def install(self):
        self.system('vcbuild.bat')
        self.bin('Release\\node.exe')
        self.bin('deps\\npm\\bin\\npm')
        self.bin('deps\\npm\\bin\\npm.cmd')
        self.cd('deps')
        self.copy('npm', 'bin\\node_modules\\npm')

    def test(self):
        self.system('node -v')
