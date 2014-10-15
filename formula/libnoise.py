
import winbrew

class Libnoise(winbrew.Formula):
    url = 'https://github.com/eXpl0it3r/libnoise.git'
    homepage = 'http://libnoise.sourceforge.net/glossary/index.html'
    sha1 = 'c0fb4c67899fe2877d817e48eb7e58b03472a9a0'
    build_deps = ('cmake',)
    deps = ()

    def install(self):
        self.cmake(winbrew.cmake_args)
        self.msbuild(winbrew.msbuild_args+('libnoise.sln',))
        self.lib('Release\\libnoise.lib')
        self.includes('include')

    def test(self):
        pass
