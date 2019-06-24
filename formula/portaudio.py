
import winbrew

class Portaudio(winbrew.Formula):
    url = 'http://www.portaudio.com/archives/pa_stable_v190600_20161030.tgz'
    homepage = ''
    sha1 = '56c596bba820d90df7d057d8f6a0ec6bf9ab82e8'
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
