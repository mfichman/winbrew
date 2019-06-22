
import winbrew
import os
import shutil

class Csfml(winbrew.Formula):
    url = 'https://github.com/SFML/CSFML/archive/2.3.zip'
    homepage = 'http://www.sfml-dev.org'
    sha1 = 'a710dc1bfc0bfa9d7bf9296718653498f0a6fead'
    build_deps = ('cmake','sfml',)
    deps = ()

    options = {
        'build-examples': 'Build example programs',
    }

    def build(self):
        self.cmake_build('build', winbrew.cmake_args+(
             '-DSFML_BUILD_EXAMPLES=%s' % ('ON' if self.option('build-examples') else 'OFF'),
             '-DBUILD_SHARED_LIBS=TRUE',
        ))

    def install(self):
        self.lib('build\\lib\\Release\\csfml-audio-2.dll', 'csfml-audio.dll')
        self.lib('build\\lib\\Release\\csfml-graphics-2.dll', 'csfml-graphics.dll')
        self.lib('build\\lib\\Release\\csfml-network-2.dll', 'csfml-network.dll')
        self.lib('build\\lib\\Release\\csfml-window-2.dll', 'csfml-window.dll')
        self.lib('build\\lib\\Release\\csfml-system-2.dll', 'csfml-system.dll')
        self.includes('include')

    def test(self):
        pass
