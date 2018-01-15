
import winbrew

class Apitrace(winbrew.Formula):
    url = 'https://github.com/apitrace/apitrace/archive/7.1.zip'
    homepage = 'https://apitrace.github.io'
    sha1 = '27c68e4aa8cec986755cb915e2aca38cd55b7233'
    build_deps = ('cmake', 'zlib', 'libpng', 'qt5')
    deps = ()

    def install(self):
        self.cmake_build('build', winbrew.cmake_args+(
            '-DENABLE_GUI=TRUE'
        ))
        self.bin('build/Release/apitrace.exe')
        self.bin('build/Release/d3dretrace.exe')
        self.bin('build/Release/glretrace.exe')

    def test(self):
        pass
