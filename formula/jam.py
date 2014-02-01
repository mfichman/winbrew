import winbrew

class Jam(winbrew.Formula):
    url = 'http://downloads.sourceforge.net/project/freetype/ftjam/2.5.2/ftjam-2.5.2-win32.zip'
    homepage = 'http://www.perforce.com/documentation/jam'
    sha1 = ''
    build_deps = ()
    deps = ()

    def install(self):
        self.bin('jam.exe')

    def test(self):
        pass
