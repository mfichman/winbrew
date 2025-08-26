import winbrew
import os

class Glfw(winbrew.Formula):
    url = 'https://github.com/glfw/glfw/releases/download/3.3.8/glfw-3.3.8.zip'
    homepage = 'http://www.glfw.org'
    sha1 = '15409a1d658e2ae2d3e3ac1048e7e011cb65edc5'
    build_deps = ('cmake',)
    deps = ()
    options = {
        'build-examples': 'Build example programs',
        'build-tests': 'Build tests',
        'build-docs': 'Build documentation',
        'shared': 'Build shared libraries',
    }

    def patch(self):
        pass

    def build(self):
        self.cmake_build('build', winbrew.cmake_args+(
            '-DBUILD_SHARED_LIBS=%s' % ('ON' if self.option('shared') else 'OFF'),
            '-DGLFW_BUILD_EXAMPLES=%s' % ('ON' if self.option('build-examples') else 'OFF'),
            '-DGLFW_BUILD_TESTS=%s' % ('ON' if self.option('build-tests') else 'OFF'),
            '-DGLFW_BUILD_DOCS=%s' % ('ON' if self.option('build-docs') else 'OFF'),
        ))

    def install(self):
        self.includes('include\\GLFW', 'GLFW')
        self.lib('build\\src\\Release\\glfw3.lib', 'glfw.lib')
