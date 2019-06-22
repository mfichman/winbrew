import winbrew
import shutil
import os

class Sfml(winbrew.Formula):
    url = 'https://github.com/SFML/SFML/archive/2.3.2.zip'
    homepage = 'http://www.sfml-dev.org'
    sha1 = '8dfcf39ee08238cba6fd391a91aac803d670cb79'
    build_deps = ('cmake',)
    deps = ('glew', 'freetype2', 'jpeg', 'openal', 'flac', 'vorbis')

    options = {
        'build-examples': 'Build example programs',
    }

    def broken_extlibs_workaround(self):
        # Remove the extlibs that are packaged w/ the SFML source. WinBrew
        # builds these extlibs itself.
        if os.path.exists('extlibs\\libs-msvc'):
            shutil.rmtree('extlibs\\libs-msvc')

    def build(self):
        self.broken_extlibs_workaround()
        self.patch(PATCH_FIND_VORBIS)
        self.cmake_build('build-static', winbrew.cmake_args+(
            '-DJPEG_INCLUDE_DIR=%s' % winbrew.include_path,
            '-DCMAKE_INCLUDE_DIR=%s' % winbrew.include_path,
            '-DCMAKE_LIBRARY_DIR=%s' % winbrew.include_path,
            '-DSFML_BUILD_EXAMPLES=%s' % ('ON' if self.option('build-examples') else 'OFF'),
            '-DBUILD_SHARED_LIBS=OFF',
        ))
        self.cmake_build('build-shared', winbrew.cmake_args+(
            '-DJPEG_INCLUDE_DIR=%s' % winbrew.include_path,
            '-DCMAKE_INCLUDE_DIR=%s' % winbrew.include_path,
            '-DCMAKE_LIBRARY_DIR=%s' % winbrew.include_path,
            '-DSFML_BUILD_EXAMPLES=%s' % ('ON' if self.option('build-examples') else 'OFF'),
            '-DBUILD_SHARED_LIBS=ON',
        ))

    def install(self):
        self.lib('build-static\\lib\\Release\\sfml-audio-s.lib')
        self.lib('build-static\\lib\\Release\\sfml-graphics-s.lib')
        self.lib('build-static\\lib\\Release\\sfml-network-s.lib')
        self.lib('build-static\\lib\\Release\\sfml-window-s.lib')
        self.lib('build-static\\lib\\Release\\sfml-system-s.lib')
        # Installs the files twice: once with the 's' suffix, so csfml can find the file.

        self.lib('build-shared\\lib\\Release\\sfml-audio.lib')
        self.lib('build-shared\\lib\\Release\\sfml-graphics.lib')
        self.lib('build-shared\\lib\\Release\\sfml-network.lib')
        self.lib('build-shared\\lib\\Release\\sfml-window.lib')
        self.lib('build-shared\\lib\\Release\\sfml-system.lib')

        self.lib('build-shared\\lib\\Release\\sfml-audio-2.dll')
        self.lib('build-shared\\lib\\Release\\sfml-graphics-2.dll')
        self.lib('build-shared\\lib\\Release\\sfml-network-2.dll')
        self.lib('build-shared\\lib\\Release\\sfml-window-2.dll')
        self.lib('build-shared\\lib\\Release\\sfml-system-2.dll')

        self.includes('include')
        self.copy('cmake\\Modules', 'share\\cmake-3.4\\Modules')

    def test(self):
        pass

PATCH_FIND_VORBIS = """
--- cmake\Modules\FindVorbis.cmake
+++ cmake\Modules\FindVorbis.cmake
@@ -13,7 +13,6 @@
 find_library(OGG_LIBRARY NAMES ogg)
 find_library(VORBIS_LIBRARY NAMES vorbis)
 find_library(VORBISFILE_LIBRARY NAMES vorbisfile)
-find_library(VORBISENC_LIBRARY NAMES vorbisenc)

 include(FindPackageHandleStandardArgs)
 find_package_handle_standard_args(VORBIS DEFAULT_MSG VORBIS_LIBRARY VORBISFILE_LIBRARY VORBISENC_LIBRARY OGG_LIBRARY VORBIS_INCLUDE_DIR OGG_INCLUDE_DIR)

--- cmake\Modules\FindSFML.cmake
+++ cmake\Modules\FindSFML.cmake
@@ -330,7 +330,6 @@
         find_sfml_dependency(OGG_LIBRARY "Ogg" ogg)
         find_sfml_dependency(VORBIS_LIBRARY "Vorbis" vorbis)
         find_sfml_dependency(VORBISFILE_LIBRARY "VorbisFile" vorbisfile)
-        find_sfml_dependency(VORBISENC_LIBRARY "VorbisEnc" vorbisenc)
         find_sfml_dependency(FLAC_LIBRARY "FLAC" FLAC)

         # update the list
"""
