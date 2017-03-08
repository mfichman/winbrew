import winbrew
import os

class Glfw(winbrew.Formula):
    url = 'https://github.com/glfw/glfw/releases/download/3.2.1/glfw-3.2.1.zip'
    homepage = 'http://www.glfw.org'
    sha1 = 'd40d8d491e53c105a01a02b4b53242ab7b2d27c3'
    build_deps = ('cmake',)
    deps = ()
    options = {
        'build-examples': 'Build example programs',
        'build-tests': 'Build tests',
        'build-docs': 'Build documentation',
        'shared': 'Build shared libraries',
    }

    def install(self):
        self.cmake_build('build', winbrew.cmake_args+(
            '-DBUILD_SHARED_LIBS=%s' % ('ON' if self.option('shared') else 'OFF'),
            '-DGLFW_BUILD_EXAMPLES=%s' % ('ON' if self.option('build-examples') else 'OFF'),
            '-DGLFW_BUILD_TESTS=%s' % ('ON' if self.option('build-tests') else 'OFF'),
            '-DGLFW_BUILD_DOCS=%s' % ('ON' if self.option('build-docs') else 'OFF'),
        ))
        self.includes('include\\GLFW', 'GLFW')
        self.lib('build\\src\\Release\\glfw3.lib', 'glfw.lib')
