import winbrew

class Freetype2(winbrew.Formula):
    url = 'http://downloads.sourceforge.net/project/freetype/freetype2/2.5.2/freetype-2.5.2.tar.bz2'
    homepage = 'http://freetype.org'
    sha1 = ''
    build_deps = ('cmake',)
    deps = ()

    options = {
        'debug': 'Build debug libraries', 
    }

    def install(self):
        self.cmake(('-G', 'Visual Studio 12'))
        config = '/p:Configuration=%s' % ('Debug' if self.option('debug') else 'Release')
        self.msbuild(winbrew.msbuild_args+('freetype.vcxproj',config))
        self.libs('Debug' if self.option('debug') else 'Release')
        self.includes('include')

    def test(self):
        pass
