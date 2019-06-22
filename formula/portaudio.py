
import winbrew

class Portaudio(winbrew.Formula):
    url = 'http://www.portaudio.com/archives/pa_stable_v19_20140130.tgz'
    homepage = ''
    sha1 = '526a7955de59016a06680ac24209ecb6ce05527d'
    build_deps = ()
    deps = ()

    def build(self):
        self.cmake_build('bld')

    def install(self):
        self.lib(r'bld\Release\portaudio_x64.dll', 'portaudio_x64.dll')
        self.lib(r'bld\Release\portaudio_x64.lib', 'portaudio.lib')
        self.lib(r'bld\Release\portaudio_x64.exp', 'portaudio.exp')
        self.lib(r'bld\Release\portaudio_static_x64.lib', 'portaudio-static.lib')
        self.includes('include')

    def test(self):
        pass
