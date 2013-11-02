import winbrew

class Sfr(winbrew.Formula):
    url = 'https://github.com/mfichman/simple-fast-renderer.git'
    homepage = 'https://github.com/mfichman/simple-fast-renderer'
    sha1 = ''
    build_deps = ()
    deps = ('')

    def install(self):
        self.scons() 
        self.libs('lib')
        self.include('include')

    def test(self):
        pass
