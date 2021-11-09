
import winbrew

class Portaudio(winbrew.Formula):
    url = 'http://files.portaudio.com/archives/pa_stable_v190700_20210406.tgz'
    homepage = 'https://portaudio.com'
    sha1 = 'b7e9b9c53d993f6d110487ef56a3d4529d21b2f1'
    build_deps = ('cmake',)
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
