import winbrew

class Box2D(winbrew.Formula):
    url = 'https://box2d.googlecode.com/files/Box2D_v2.2.1.zip'
    homepage = ''
    sha1 = ''
    build_deps = ()
    deps = ('')

    def install(self):
        self.cd('Box2D_v2.2.1\\Build\\vs2010')
        self.msbuild(winbrew.msbuild_args+('Box2D.vcxproj',))
        self.libs('bin\\Release')
        self.includes('..\\..\\Box2D', dest='Box2D')

    def test(self):
        pass
