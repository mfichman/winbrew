import winbrew

class Jam(winbrew.Formula):
    url = 'http://downloads.sourceforge.net/project/freetype/ftjam/2.5.2/ftjam-2.5.2-win32.zip'
    homepage = 'http://www.perforce.com/documentation/jam'
    sha1 = '710a50ce2345dfc5a90f2749ecd1a01fd4b2ae41'
    build_deps = ()
    deps = ()

    def install(self):
        self.bin('jam.exe')

    def test(self):
        self.system('jam -v')
