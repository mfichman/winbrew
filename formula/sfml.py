import winbrew

class Sfml(winbrew.Formula):
    url = 'https://github.com/SFML/SFML/archive/2.3.2.zip'
    homepage = 'http://www.sfml-dev.org'
    sha1 = '8dfcf39ee08238cba6fd391a91aac803d670cb79'
    build_deps = ('cmake',)
    deps = ('glew', 'freetype2', 'jpeg', 'openal')
    
    options = {
        'build-examples': 'Build example programs',
    }

    def install(self):
        self.cmake_build('build-static', winbrew.cmake_args+(
            '-DSFML_BUILD_EXAMPLES=%s' % ('ON' if self.option('build-examples') else 'OFF'),
            '-DBUILD_SHARED_LIBS=OFF',
        ))
        self.cmake_build('build-shared', winbrew.cmake_args+(
            '-DSFML_BUILD_EXAMPLES=%s' % ('ON' if self.option('build-examples') else 'OFF'),
            '-DBUILD_SHARED_LIBS=ON',
        ))

        self.lib('build-static\\lib\\Release\\sfml-audio-s.lib', 'sfml-audio.lib')
        self.lib('build-static\\lib\\Release\\sfml-graphics-s.lib', 'sfml-graphics.lib')
        self.lib('build-static\\lib\\Release\\sfml-network-s.lib', 'sfml-network.lib')
        self.lib('build-static\\lib\\Release\\sfml-window-s.lib', 'sfml-window.lib')
        self.lib('build-static\\lib\\Release\\sfml-system-s.lib', 'sfml-system.lib')
        # Installs the files twice: once with the 's' suffix, so csfml can find the file.

        self.lib('build-shared\\lib\\Release\\sfml-audio-2.dll', 'sfml-audio.dll')
        self.lib('build-shared\\lib\\Release\\sfml-graphics-2.dll', 'sfml-graphics.dll')
        self.lib('build-shared\\lib\\Release\\sfml-network-2.dll', 'sfml-network.dll')
        self.lib('build-shared\\lib\\Release\\sfml-window-2.dll', 'sfml-window.dll')
        self.lib('build-shared\\lib\\Release\\sfml-system-2.dll', 'sfml-system.dll')

        self.includes('include')
        self.copy('cmake\\Modules', 'share\\cmake-2.8\\Modules')

    def test(self):
        pass
