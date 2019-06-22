
import winbrew

class Emscripten(winbrew.Formula):
    url = 'https://github.com/emscripten-core/emsdk.git'
    homepage = 'https://github.com/emscripten-core/emsdk'
    sha1 = '6eb6c5d80271cb61dbbdc3c0bb45feb134032032'
    build_deps = ()
    deps = ()

    def build(self):
        self.system('emsdk install latest', shell=True)
        self.system('emsdk activate latest', shell=True)
        self.system('emsdk_env.bat', shell=True)

    def install(self):
        self.bin('emsdk')
        self.bin('emsdk.bat')
        self.bin('emsdk_env.bat')
        self.bin('emsdk_manifest.json')
        self.bin('emscripten-releases-tags.txt')

    def test(self):
        pass
