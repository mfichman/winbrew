import winbrew

class Jam(winbrew.Formula):
    url = 'http://downloads.sourceforge.net/project/freetype/ftjam/2.5.2/ftjam-2.5.2-win32.zip'
    homepage = 'http://www.perforce.com/documentation/jam'
    sha1 = '15b4dab6f5f7addf5f35b4d4946f043a81d554f0'
    build_deps = ()
    deps = ()

    def install(self):
        self.bin('jam.exe')

    def test(self):
        self.system('jam -v')
