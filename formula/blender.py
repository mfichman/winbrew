
import winbrew

class Blender(winbrew.Formula):
    url = 'http://download.blender.org/source/blender-2.77a.tar.gz'
    homepage = 'http://www.blender.org'
    sha1 = '935793b3e9fd4d02c71f275aac3aca27cd58bdfb'
    build_deps = ()
    deps = ()

    def install(self):
        self.cmake_build('build', winbrew.cmake_args)

    def test(self):
        self.system('blender -v')
