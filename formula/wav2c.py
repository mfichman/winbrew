
import winbrew

class Wav2C(winbrew.Formula):
    url = 'https://github.com/mfichman/wav2c.git'
    homepage = 'https://github.com/mfichman/wav2c'
    sha1 = '3b4b365112e6d5b93716ff857c5aaa3a6b737859'
    build_deps = ()
    deps = ()

    def install(self):
        self.system('cl.exe main.c wavdata.c /Fe:wav2c')
        self.bin('wav2c.exe')

    def test(self):
        pass
