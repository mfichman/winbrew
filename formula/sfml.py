import winbrew

class Sfml(winbrew.Formula):
    url = 'https://github.com/LaurentGomila/SFML/archive/2.1.zip'
    homepage = 'http://sfml-dev.org'
    sha1 = ''
    build_deps = ('cmake',)
    deps = ()

    def install(self):
        self.cmake()
        self.nmake()
        self.libs('lib')
        self.includes('include')

    def test(self):
        pass
