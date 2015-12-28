import winbrew

class Nodejs(winbrew.Formula):
    url = 'http://nodejs.org/dist/v4.2.4/node-v4.2.4.tar.gz'
    homepage = 'https://nodejs.org'
    sha1 = '3cfef84f3a80b9e8835f8bee5a8209a4af8c52f2'
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
