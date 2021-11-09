
import winbrew

class Ninja(winbrew.Formula):
    url = 'https://github.com/ninja-build/ninja/releases/download/v1.10.2/ninja-win.zip'
    homepage = 'https://ninja-build.org'
    sha1 = 'ccacdf88912e061e0b527f2e3c69ee10544d6f8a'
    build_deps = ()
    deps = ()

    def build(self):
        pass

    def install(self):
        self.bin('ninja.exe')

    def test(self):
        pass
