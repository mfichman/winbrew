import winbrew

class Freetype2(winbrew.Formula):
    url = 'http://downloads.sourceforge.net/project/freetype/freetype2/2.5.2/freetype-2.5.2.tar.bz2'
    homepage = 'http://freetype.org'
    sha1 = ''
    build_deps = ('cmake',)
    deps = ()

    def install(self):
        #self.cmake(('-G', 'Visual Studio 12'))
        #self.msbuild(winbrew.msbuild_args+('freetype.sln',))
        #self.includes('include')
        #self.libs('Release')
        self.system('jam')

    def test(self):
        pass
