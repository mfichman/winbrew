import winbrew

class Sfr(winbrew.Formula):
    url = 'https://github.com/mfichman/simple-fast-renderer.git'
    homepage = 'https://github.com/mfichman/simple-fast-renderer'
    sha1 = 'd6f041015fb57c17c9df0a4406ead099bbc10f4d'
    build_deps = ('scons',)
    deps = ('glew','sfml','freetype2')

    def install(self):
        self.scons() 
        self.libs('lib')
        self.includes('include')

    def test(self):
        pass
