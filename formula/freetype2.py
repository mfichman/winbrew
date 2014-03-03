import winbrew

class Freetype2(winbrew.Formula):
    url = 'http://downloads.sourceforge.net/project/freetype/freetype2/2.5.2/freetype-2.5.2.tar.bz2'
    homepage = 'http://freetype.org'
    sha1 = ''
    build_deps = ('jam',)
    deps = ()

    def install(self):
        self.includes('include')
        self.libs('objs')
        self.system('jam -sJAM_TOOLSET=VISUALC')

    def test(self):
        pass
