import winbrew

class Premake(winbrew.Formula):
    url = 'http://downloads.sourceforge.net/project/premake/Premake/4.3/premake-4.3-src.zip'
    homepage = 'http://premake.sourceforge.net'
    sha1 = '8f37a3599121580f18b578811162b9b49a2e122f'
    build_deps = ()
    deps = ('')

    def build(self):
        self.cd('build\\vs2010')
        self.msbuild()

    def install(self):
        self.cd('bin\\release')
        self.bin('premake4.exe')

    def test(self):
        self.system('premake4 --version')
