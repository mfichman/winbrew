
import winbrew

class Wav2C(winbrew.Formula):
    url = 'https://github.com/mfichman/wav2c.git'
    homepage = 'https://github.com/mfichman/wav2c'
    sha1 = '294b33b23eb259ec31fb73659b0c132e8efae83e'
    build_deps = ()
    deps = ()

    def install(self):
        self.system('cl.exe main.c wavdata.c /Fe:wav2c')
        self.bin('wav2c.exe')

    def test(self):
        pass
