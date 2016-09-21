import winbrew
import sys
import os

class Blender(winbrew.Formula):
    url = 'http://download.blender.org/source/blender-2.77a.tar.gz'
    homepage = 'http://www.blender.org'
    sha1 = '935793b3e9fd4d02c71f275aac3aca27cd58bdfb'
    build_deps = ()
    deps = ()

    options = {
        'python-35-dir': 'Path to a Python 3.5 installation',
    }

    def install(self):
        python_35_dir = self.option('python-35-dir') or 'D:\\Tools\\Python35'
        self.cmake_build('build', winbrew.cmake_args+(
            '-DLIBDIR={0}'.format(winbrew.config.lib_path),
            '-DPYTHON_INCLUDE_DIR={0}'.format(os.path.join(python_35_dir, 'include')),
        ))

    def test(self):
        self.system('blender -v')
