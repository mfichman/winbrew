import winbrew

class Bullet(winbrew.Formula):
    url = 'https://bullet.googlecode.com/files/bullet-2.82-r2704.zip'
    homepage = 'http://bulletphysics.org'
    sha1 = ''
    build_deps = ('cmake',)
    deps = ()
    options = {
        'double-precision': 'Use double precision',
        'build-demo': 'Build demo application',
        'build-extra': 'Build extra library',
        'shared': 'Build shared libraries',
    }

    def install(self):
        self.cd('bullet-2.82-r2704')
        args = ['-G', 'Visual Studio 12']

        self.cmake(('-G', 'Visual Studio 12', 
            '-DUSE_DOUBLE_PRECISION=%s' % ('ON' if self.option('double-precision') else 'OFF'), 
            '-DBUILD_DEMOS=%s' % ('ON' if self.option('build-demos') else 'OFF'),
            '-DBUILD_EXTRAS=%s' % ('ON' if self.option('build-extras') else 'OFF'),
            '-DBUILD_SHARED_LIBS=%s' % ('ON' if self.option('shared') else 'OFF',
        ))
        self.msbuild(winbrew.msbuild_args+('BULLET_PHYSICS.sln',))
        self.libs('lib\\Release')
        self.includes('src', dest='bullet')

    def test(self):
        pass
