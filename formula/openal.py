import winbrew

class Openal(winbrew.Formula):
    url = 'https://www.openal-soft.org/openal-releases/openal-soft-1.21.1.tar.bz2'
    homepage = 'https://www.openal-soft.org'
    sha1 = 'f39b81a9ce22419e106259cf424405291520b8f3'
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
