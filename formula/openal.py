import winbrew

class Openal(winbrew.Formula):
    url = 'http://kcat.strangesoft.net/openal-releases/openal-soft-1.15.1.tar.bz2'
    homepage = 'http://kcat.strangesoft.net/openal.html'
    sha1 = 'a0e73a46740c52ccbde38a3912c5b0fd72679ec8'
    build_deps = ('cmake',)
    deps = ()

    def install(self): 
        self.cmake(winbrew.cmake_args)
        self.msbuild(winbrew.msbuild_args+('OpenAL32.vcxproj',))
        self.includes('include')
        self.libs('Release')

    def test(self):
        pass
