
import winbrew

class Picoc(winbrew.Formula):
    url = 'https://github.com/zsaleeba/picoc/archive/master.zip'
    homepage = 'https://github.com/zsaleeba/picoc'
    sha1 = 'b2e70b9e85f1ff490ff9aaf3ccdf0d06a6c19f9c'
    build_deps = ()
    deps = ()

    def install(self):
        self.cd('msvc\\picoc')
        self.msbuild()
        self.bin('Release\\picoc.exe')

    def test(self):
        pass
