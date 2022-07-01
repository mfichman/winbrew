
import winbrew

class Glslang(winbrew.Formula):
    url = 'https://github.com/KhronosGroup/glslang/archive/refs/tags/11.6.0.zip'
    homepage = 'https://github.com/KhronosGroup/glslang'
    sha1 = '21935279a2eeeef1aca82675815885b7845259bb'
    build_deps = ('cmake',)
    deps = ()

    def build(self):
        self.cmake_build('build', winbrew.cmake_args)

    def install(self):
        self.bin('build\\StandAlone\\Release\\glslangValidator.exe')

    def test(self):
        pass
