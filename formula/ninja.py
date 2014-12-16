
import winbrew

class Ninja(winbrew.Formula):
    url = 'git://github.com/martine/ninja.git'
    homepage = ''
    sha1 = '6e5eb247e6df6fbce1a3e99fa45df6e3ed596394'
    build_deps = ()
    deps = ()

    def install(self):
        self.system('python configure.py --bootstrap')
        self.bin('ninja.exe')

    def test(self):
        self.system('ninja -v')
