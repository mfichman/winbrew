import winbrew

class Glew(winbrew.Formula):
    url = 'http://downloads.sourceforge.net/project/glew/glew/1.10.0/glew-1.10.0.zip'
    homepage = 'http://glew.sourceforge.net'
    sha1 = ''
    build_deps = ()
    deps = ()

    def install(self):
        self.cd('glew-1.10.0')
        self.msbuild(winbrew.msbuild_args+('build\\vc10\\glew_static.vcxproj',))
        self.libs('lib\\Release\\Win32')
        self.includes('include')

    def test(self):
        pass
