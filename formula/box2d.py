import winbrew

class Box2d(winbrew.Formula):
    url = 'https://box2d.googlecode.com/files/Box2D_v2.2.1.zip'
    homepage = ''
    sha1 = ''
    build_deps = ('premake')
    deps = ('')

    def install(self):
        self.cd('Box2D_v2.2.1')
        pass

    def test(self):
        pass
