
import winbrew

class Glslang(winbrew.Formula):
    url = 'https://github.com/KhronosGroup/glslang/archive/7.8.2853.zip'
    homepage = 'https://github.com/KhronosGroup/glslang'
    sha1 = '8f7e1ba2bab166e39182790974564d27d6d628c8'
    build_deps = ('cmake',)
    deps = ()

    def install(self):
        self.cmake_build('build', winbrew.cmake_args)
        self.bin('build\\StandAlone\\Release\\glslangValidator.exe')

    def test(self):
        pass
