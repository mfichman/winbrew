import winbrew

class Sfml(winbrew.Formula):
    url = 'https://github.com/LaurentGomila/SFML/archive/2.1.zip'
    homepage = 'http://sfml-dev.org'
    sha1 = ''
    build_deps = ('cmake',)
    deps = ()
    
    options = {
        'build-examples': 'Build example programs',
        'debug': 'Build debug libraries', 
    }

    def install(self):
        self.cmake(('-G', 'Visual Studio 12',
            '-DSFML_BUILD_EXAMPLES=%s' % ('ON' if self.option('build-examples') else 'OFF'),
            #'-DSFML_USE_STATIC_STD_LIBS=%s' % ('OFF' if self.option('shared') else 'ON'),
        ))
        config = '/p:Configuration=%s' % ('Debug' if self.option('debug') else 'Release')
        self.msbuild(winbrew.msbuild_args+('SFML.sln',config))
        self.libs('lib\\%s' % ('Debug' if self.option('debug') else 'Release'))
        self.includes('include')

    def test(self):
        pass
