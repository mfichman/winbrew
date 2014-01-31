import winbrew

class Freetype2(winbrew.Formula):
    url = 'http://downloads.sourceforge.net/project/freetype/freetype2/2.5.2/freetype-2.5.2.tar.bz2'
    homepage = 'http://freetype.org'
    sha1 = ''
    build_deps = ()
    deps = ('')

    def install(self):
        self.cd('freetype-2.5.2')
        self.cmake(('-G', 'Visual Studio 12'))
        self.msbuild(winbrew.msbuild_args+('freetype.sln',))
        self.includes('include', 'freetype2')
        self.libs('Release')

    def test(self):
        pass
