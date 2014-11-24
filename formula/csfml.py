
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
    }

    def install(self):
        os.environ['PATH'] = ';'.join((
            os.path.join(winbrew.cache_path, 'sfml\\sfml-master\\extlibs\\libs-msvc\\x86'),
            os.path.join(winbrew.cache_path, 'sfml\\sfml-master\\build-static\\lib\\Release'),
            os.environ.get('PATH', ''),
        ))
        
        self.cmake_build('build', winbrew.cmake_args+(
             '-DSFML_BUILD_EXAMPLES=%s' % ('ON' if self.option('build-examples') else 'OFF'),
             '-DBUILD_SHARED_LIBS=TRUE',
        ))
        self.lib('build\\lib\\Release\\csfml-audio-2.dll', 'csfml-audio.dll')
        self.lib('build\\lib\\Release\\csfml-graphics-2.dll', 'csfml-graphics.dll')
        self.lib('build\\lib\\Release\\csfml-network-2.dll', 'csfml-network.dll')
        self.lib('build\\lib\\Release\\csfml-window-2.dll', 'csfml-window.dll')
        self.lib('build\\lib\\Release\\csfml-system-2.dll', 'csfml-system.dll')
        self.includes('include')

    def test(self):
        pass
