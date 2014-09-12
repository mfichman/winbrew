import winbrew

class Premake(winbrew.Formula):
    url = 'http://downloads.sourceforge.net/project/premake/Premake/4.3/premake-4.3-src.zip'
    homepage = 'http://premake.sourceforge.net'
    sha1 = '1c9c19bbca17ec02cb55212304b4d8e99b35c8fa'
    build_deps = ()
    deps = ('')

    def install(self):
        self.cd('build\\vs2010')
        self.msbuild()
        self.cd('..\\..\\bin\\release')
        self.bin('premake4.exe')

    def test(self):
        self.system('premake4 --version')
