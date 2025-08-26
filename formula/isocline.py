
import winbrew

class Isocline(winbrew.Formula):
    url = 'https://github.com/daanx/isocline.git'
    homepage = ''
    sha1 = '93c0f58f96f463940b3e54409512437dd7574dac'
    build_deps = ()
    deps = ()

    def build(self):
        self.cmake_build('build')

    def install(self):
        self.lib('build//Release//isocline.lib')	
        self.include('include/isocline.h')

    def test(self):
        pass
