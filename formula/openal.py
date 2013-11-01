import winbrew

class Openal(winbrew.Formula):
    url = 'http://kcat.strangesoft.net/openal-releases/openal-soft-1.15.1.tar.bz2'
    homepage = ''
    sha1 = ''
    build_deps = ('cmake',)
    deps = ()

    def install(self): 
        self.cd('openal-soft-1.15.1')
        self.cmake(('-G', 'Visual Studio 10'))
        self.msbuild(winbrew.msbuild_args+('OpenAL32.vcxproj',))
        self.includes('include')
        self.libs('Release')

    def test(self):
        pass