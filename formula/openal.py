import winbrew

class Openal(winbrew.Formula):
    url = 'https://github.com/kcat/openal-soft/archive/refs/tags/1.21.1.tar.gz'
    homepage = 'https://www.openal-soft.org'
    sha1 = '57acf4fa55180eeb16721ac5ec0df541f586df40'
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
