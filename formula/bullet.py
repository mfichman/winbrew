import winbrew

class Bullet(winbrew.Formula):
    url = 'https://bullet.googlecode.com/files/bullet-2.82-r2704.zip'
    homepage = 'http://bulletphysics.org'
    sha1 = 'f4b3332ad074aef3f8c1b731c1b7b385d3386d31'
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
            '-DBUILD_EXTRAS=%s' % ('ON' if self.option('build-extras') else 'OFF'),
            '-DUSE_MSVC_RUNTIME_LIBRARY_DLL=ON',
        )

        self.cmake_build('build', winbrew.cmake_args+cmake_args+(
            '-DBUILD_SHARED_LIBS=OFF',
        ))
        self.libs('build\\lib\\Release')
        self.includes('src', dest='bullet')

    def test(self):
        pass
