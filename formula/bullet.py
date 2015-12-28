import winbrew

class Bullet(winbrew.Formula):
    url = 'https://github.com/bulletphysics/bullet3/archive/2.83.5.zip'
    homepage = 'http://bulletphysics.org'
    sha1 = '7058cc08b0dacb0441b47f4d91c9df8d92c67187'
    build_deps = ('cmake',)
    deps = ()
    options = {
        'double-precision': 'Use double precision',
        'build-demos': 'Build demo application',
        'build-extras': 'Build extra library',
    }

    def install(self):
        cmake_args = (
            '-DUSE_DOUBLE_PRECISION=%s' % ('ON' if self.option('double-precision') else 'OFF'), 
            '-DBUILD_DEMOS=%s' % ('ON' if self.option('build-demos') else 'OFF'),
            '-DBUILD_BULLET2_DEMOS=%s' % ('ON' if self.option('build-extras') else 'OFF'),
            '-DBUILD_BULLET3_=OFF',
            '-DBUILD_SHARED_LIBS=OFF',
            '-DUSE_MSVC_RUNTIME_LIBRARY_DLL=ON',
        )

        self.cmake_build('build', winbrew.cmake_args+cmake_args)
        self.libs('build\\lib\\Release')
        self.includes('src', dest='bullet')

    def test(self):
        pass
