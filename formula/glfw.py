import winbrew
import os

class Glfw(winbrew.Formula):
    url = 'https://github.com/glfw/glfw/archive/018ab7229b710be1da4edd289de499c0d99c38c0.zip'
    homepage = 'http://www.glfw.org'
    sha1 = 'fa00828b2514b76399b3a91fcf411786f84074ce'
    build_deps = ('cmake',)
    deps = ()
    options = {
        'build-examples': 'Build example programs',
        'build-tests': 'Build tests',
        'build-docs': 'Build documentation',
        'shared': 'Build shared libraries',
    }

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
