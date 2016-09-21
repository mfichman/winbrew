import winbrew

class Box2D(winbrew.Formula):
    url = 'https://github.com/erincatto/Box2D/archive/v2.3.1.zip'
    homepage = 'http://box2d.org'
    sha1 = 'a821af6da1ffcae7e8954f7c15af5215bf644cbf'
    build_deps = ('cmake',)
    deps = ()
    options = {
        'build-demos': 'Build demo applications',
        'shared': 'Build shared libraries',
    }

    def install(self):
        self.cd('Box2D')
        self.cmake_build('build', winbrew.cmake_args+(
            '-DBOX2D_BUILD_STATIC=%s' % ('OFF' if self.option('shared') else 'ON'),
            '-DBOX2D_BUILD_EXAMPLES=%s' % ('ON' if self.option('build-demos') else 'OFF'),
            '-DCMAKE_CXX_FLAGS_RELEASE=/MT',
        ))

        self.libs('Box2D\\Release')
        self.includes('Box2D', dest='Box2D')

    def test(self):
        pass
