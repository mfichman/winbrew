import winbrew

class Box2D(winbrew.Formula):
    url = 'https://box2d.googlecode.com/files/Box2D_v2.2.1.zip'
    homepage = 'http://box2d.org'
    sha1 = 'f97e75227a19b01858b1431e5f3eb6b8827bed12'
    build_deps = ('cmake',)
    deps = ()
    options = {
        'build-demos': 'Build demo applications',
        'shared': 'Build shared libraries',
    }

    def install(self):
        self.cmake(winbrew.cmake_args+(
            '-DBOX2D_BUILD_STATIC=%s' % ('OFF' if self.option('shared') else 'ON'),
            '-DBOX2D_BUILD_DYNAMIC=%s' % ('ON' if self.option('shared') else 'OFF'),
            '-DBOX2D_BUILD_EXAMPLES=%s' % ('ON' if self.option('build-demos') else 'OFF'),
            '-DCMAKE_CXX_FLAGS_RELEASE=/MT',
        ))

        self.msbuild(winbrew.msbuild_args+('Box2D.sln','/p:RuntimeLibrary=0'))
        self.libs('Box2D\\Release')
        self.includes('Box2D', dest='Box2D')

    def test(self):
        pass
