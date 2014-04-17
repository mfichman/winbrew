import winbrew

class Bullet(winbrew.Formula):
    url = 'https://bullet.googlecode.com/files/bullet-2.82-r2704.zip'
    homepage = 'http://bulletphysics.org'
    sha1 = ''
    build_deps = ('cmake',)
    deps = ()
    options = {
        'double-precision': 'Use double precision',
        'build-demos': 'Build demo application',
        'build-extras': 'Build extra library',
        'shared': 'Build shared libraries',
        'debug': 'Build debug libraries',
    }

    def install(self):
        self.cmake(('-G', 'Visual Studio 12', 
            '-DUSE_DOUBLE_PRECISION=%s' % ('ON' if self.option('double-precision') else 'OFF'), 
            '-DBUILD_DEMOS=%s' % ('ON' if self.option('build-demos') else 'OFF'),
            '-DBUILD_EXTRAS=%s' % ('ON' if self.option('build-extras') else 'OFF'),
            '-DBUILD_SHARED_LIBS=%s' % ('ON' if self.option('shared') else 'OFF'),
        ))
        config = '/p:Configuration=%s' % ('Debug' if self.option('debug') else 'Release')
        self.msbuild(winbrew.msbuild_args+('BULLET_PHYSICS.sln',config))
        self.includes('src', dest='bullet')
        self.libs('lib\\%s' % ('Debug' if self.option('debug') else 'Release'))

    def test(self):
        pass
