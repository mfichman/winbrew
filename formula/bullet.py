import winbrew

class Bullet(winbrew.Formula):
    url = 'https://github.com/LaurentGomila/SFML/archive/2.1.zip'
    homepage = ''
    sha1 = ''
    build_deps = ('cmake',)
    deps = ()

    def install(self):
        pass
        #self.cd('bullet-2.8.2-r2704')
        #self.cmake()
        #self.nmake()

    def test(self):
        pass
