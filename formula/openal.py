import winbrew

class Openal(winbrew.Formula):
    url = 'https://kcat.strangesoft.net/openal-releases/openal-soft-1.19.1.tar.bz2'
    homepage = 'http://kcat.strangesoft.net/openal.html'
    sha1 = '849db47ec3711f0181c4462b2d204c4a3d5937d2'
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
