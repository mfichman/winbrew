
import winbrew

class Ninja(winbrew.Formula):
    url = 'https://github.com/ninja-build/ninja/archive/v1.6.0.zip'
    homepage = ''
    sha1 = 'a4dc454f421ff0e0cf193b34d03e3e20db4ebba2'
    build_deps = ()
    deps = ()

    def install(self):
        self.system('python configure.py --bootstrap')
        self.bin('ninja.exe')

    def test(self):
        self.system('ninja -v')
