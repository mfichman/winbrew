import winbrew
import os

class Sdl(winbrew.Formula):
    url = 'http://libsdl.org/release/SDL2-2.0.1.zip'
    homepage = 'http://libsdl.org'
    sha1 = ''
    build_deps = ('cmake',)
    deps = ()

    def install(self):
        self.cd('VisualC')
        self.msbuild(winbrew.msbuild_args+('SDL_VS2010.sln',))
        self.includes('include', 'SDL')

    def test(self):
        pass
