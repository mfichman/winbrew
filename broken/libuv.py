
import winbrew

class Libuv(winbrew.Formula):
    url = 'https://github.com/libuv/libuv.git'
    homepage = 'https://github.com/libuv/libuv'
    sha1 = 'ddd04e6c031059690dd305a19ac2f0768fdc2e28'
    build_deps = ()
    deps = ()

    def install(self):
        self.system('vcbuild.bat')
        

    def test(self):
        pass
