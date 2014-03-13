import winbrew
import os

class Glfw(winbrew.Formula):
    url = 'http://downloads.sourceforge.net/project/glfw/glfw/3.0.4/glfw-3.0.4.zip'
    homepage = 'http://www.glfw.org'
    sha1 = ''
    build_deps = ('cmake',)
    deps = ()
    options = {
        'build-examples': 'Build example programs',
        'build-tests': 'Build tests',
        'build-docs': 'Build documentation',
        'shared': 'Build shared libraries',
    }

    def install(self):
        self.cmake(('-G', 'Visual Studio 12',
            '-DBUILD_SHARED_LIBS=%s' % ('ON' if self.option('shared') else 'OFF'),
            '-DGLFW_BUILD_EXAMPLES=%s' % ('ON' if self.option('build-examples') else 'OFF'),
            '-DGLFW_BUILD_TESTS=%s' % ('ON' if self.option('build-tests') else 'OFF'),
            '-DGLFW_BUILD_DOCS=%s' % ('ON' if self.option('build-docs') else 'OFF'),
        ))
        self.msbuild(winbrew.msbuild_args+('GLFW.sln',))
        self.includes('include\\GLFW', 'GLFW')
        self.libs('src\\Release')