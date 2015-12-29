
import winbrew

class Libnoise(winbrew.Formula):
    url = 'https://github.com/eXpl0it3r/libnoise.git'
    homepage = 'http://libnoise.sourceforge.net/glossary/index.html'
    sha1 = 'c0fb4c67899fe2877d817e48eb7e58b03472a9a0'
    build_deps = ('cmake',)
    deps = ()

    def install(self):
        self.cmake_build('build', winbrew.cmake_args)
        self.lib('build\\Release\\libnoise.lib')
        self.includes('include')

    def test(self):
        pass
