
import winbrew

class Libnoise(winbrew.Formula):
    url = 'https://github.com/eXpl0it3r/libnoise/archive/778ac138e86afbaeef7d260c8aaea3972384b433.zip'
    homepage = 'http://libnoise.sourceforge.net/glossary/index.html'
    sha1 = 'bd16c660ac386ca55561a3e818131a2197ac320f'
    build_deps = ('cmake',)
    deps = ()

    def build(self):
        self.cmake_build('build', winbrew.cmake_args)

    def install(self):
        self.lib('build\\Release\\libnoise.lib')
        self.includes('include')

    def test(self):
        pass
