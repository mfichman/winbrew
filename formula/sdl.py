import winbrew

class Sdl(winbrew.Formula):
    url = 'http://libsdl.org/release/SDL2-2.0.1.zip'
    homepage = ''
    sha1 = ''
    build_deps = ('cmake,')
    deps = ()

    def install(self):
        self.cd('SDL2-2.0.1') 
        self.cmake()
        self.nmake()
        self.includes('include', 'SDL')

    def test(self):
        pass
