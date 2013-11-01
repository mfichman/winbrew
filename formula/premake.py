import winbrew

class Premake(winbrew.Formula):
    url = 'http://downloads.sourceforge.net/project/premake/Premake/4.3/premake-4.3-src.zip'
    homepage = ''
    sha1 = ''
    build_deps = ()
    deps = ('')

    def install(self):
        self.cd('premake-4.3\\build\\vs2010')
        self.msbuild()
        self.cd('..\\..\\bin\\release')
        self.bin('premake4.exe')

    def test(self):
        pass
