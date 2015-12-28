import winbrew

class Openal(winbrew.Formula):
    url = 'http://kcat.strangesoft.net/openal-releases/openal-soft-1.17.1.tar.bz2'
    homepage = 'http://kcat.strangesoft.net/openal.html'
    sha1 = '92b8dbba07674e11538934fc7a89dcd64ecafd40'
    build_deps = ('cmake',)
    deps = ()

    def install(self): 
        self.cmake(winbrew.cmake_args+('-DBUILD_SHARED_LIBS=OFF',))
        self.msbuild(winbrew.msbuild_args+('OpenAL32.vcxproj',))
        self.includes('include')
        self.lib('Release\\openal32.lib', 'openal.lib')

    def test(self):
        pass
