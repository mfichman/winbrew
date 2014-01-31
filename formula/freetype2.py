import winbrew

class Freetype2(winbrew.Formula):
    url = 'http://downloads.sourceforge.net/project/freetype/freetype2/2.5.2/freetype-2.5.2.tar.bz2'
    homepage = ''
    sha1 = ''
    build_deps = ()
    deps = ('')

    def install(self):
        #self.cd('Box2D_v2.2.1\\Build\\vs2010')
        #self.msbuild(winbrew.msbuild_args+('Box2D.vcxproj',))
        #self.libs('bin\\Release')
        #self.includes('..\\..\\Box2D', dest='Box2D')
        pass

    def test(self):
        pass
