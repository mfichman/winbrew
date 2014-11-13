
import winbrew
import os
import shutil

class Csfml(winbrew.Formula):
    url = 'https://github.com/LaurentGomila/CSFML/archive/master.zip'
    homepage = 'http://www.sfml-dev.org'
    sha1 = '25c23ac5993096263c1b145347e3b8459ef4065d'
    build_deps = ('cmake','sfml',)
    deps = ()

    options = {
        'build-examples': 'Build example programs',
        'debug': 'Build debug libraries', 
        'shared': 'Build shared libraries',
    }

    def install(self):
        self.cmake(winbrew.cmake_args+(
            '-DSFML_BUILD_EXAMPLES=%s' % ('ON' if self.option('build-examples') else 'OFF'),
            '-DBUILD_SHARED_LIBS=TRUE',
        ))
        config = '/p:Configuration=%s' % ('Debug' if self.option('debug') else 'Release')
        self.msbuild(winbrew.msbuild_args+('CSFML.sln', config))
        self.libs('lib\\%s' % ('Debug' if self.option('debug') else 'Release'))
        self.includes('include')

    def test(self):
        pass
