import winbrew

class Sfml(winbrew.Formula):
    url = 'https://github.com/LaurentGomila/SFML/archive/master.zip'
    homepage = 'http://www.sfml-dev.org'
    sha1 = 'b669c20d13629d73071b5153956d46d0e75f3e7a'
    build_deps = ('cmake',)
    deps = ()
    
    options = {
        'build-examples': 'Build example programs',
    }

    def install(self):
        self.cmake(winbrew.cmake_args+(
            '-DSFML_BUILD_EXAMPLES=%s' % ('ON' if self.option('build-examples') else 'OFF'),
            '-DBUILD_SHARED_LIBS=FALSE',
        ))
        self.msbuild(winbrew.msbuild_args+('SFML.sln', '/p:Configuration=Debug'))
        self.msbuild(winbrew.msbuild_args+('SFML.sln', '/p:Configuration=Release'))
        # Compile debug AND release versions, b/c CSFML requires both
        self.libs('lib\\Debug')
        self.libs('lib\\Release')
        self.libs('extlibs\\libs-msvc\\x86')
        self.includes('include')
        self.copy('cmake\\Modules', 'share\\cmake-2.8\\Modules')

    def test(self):
        pass
