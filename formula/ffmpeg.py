
import winbrew

class Ffmpeg(winbrew.Formula):
    url = 'https://github.com/GyanD/codexffmpeg/releases/download/8.1.1/ffmpeg-8.1.1-essentials_build.zip'
    homepage = 'https://ffmpeg.org'
    sha1 = '6a8351d5d06ea3bef0b418dd65af1753f184673a'
    build_deps = ()
    deps = ()

    def build(self):
        pass

    def install(self):
        self.bin('bin\\ffmpeg.exe')
        self.bin('bin\\ffplay.exe')
        self.bin('bin\\ffprobe.exe')

    def test(self):
        self.system('ffmpeg -version')
