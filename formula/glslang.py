
import winbrew

class Glslang(winbrew.Formula):
    url = 'https://github.com/KhronosGroup/glslang/archive/3.0.zip'
    homepage = 'https://github.com/KhronosGroup/glslang'
    sha1 = '480ad28bb80d95615bf9d16f6e3bd45d8d7c977f'
    build_deps = ('cmake',)
    deps = ()

    def install(self):
        self.cmake_build('build', winbrew.cmake_args)
        self.bin('Install\\Windows\\glslangValidator.exe')

    def test(self):
        pass
