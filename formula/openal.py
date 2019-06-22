import winbrew

class Openal(winbrew.Formula):
    url = 'http://kcat.strangesoft.net/openal-releases/openal-soft-1.17.1.tar.bz2'
    homepage = 'http://kcat.strangesoft.net/openal.html'
    sha1 = '92b8dbba07674e11538934fc7a89dcd64ecafd40'
    build_deps = ('cmake',)
    deps = ()

    def build(self):
        self.cmake_build('build', winbrew.cmake_args+(
            '-DBUILD_SHARED_LIBS=OFF',
            '-DALSOFT_EXAMPLES=OFF',
            '-DALSOFT_BACKEND_PORTAUDIO=OFF'
        ))

    def install(self):
        self.includes('include\\AL','AL')
        self.lib('build\\Release\\openal32.lib', 'openal.lib')

    def test(self):
        pass
