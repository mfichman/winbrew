import winbrew

class Bullet(winbrew.Formula):
    url = 'https://bullet.googlecode.com/files/bullet-2.82-r2704.zip'
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
