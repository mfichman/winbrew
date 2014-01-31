import winbrew

class Glew(winbrew.Formula):
    url = 'http://downloads.sourceforge.net/project/glew/glew/1.10.0/glew-1.10.0.zip'
    homepage = 'http://glew.sourceforge.net'
    sha1 = ''
    build_deps = ()
    deps = ()

    def install(self):
        # Workaround for broken RC compiler in Visual Studio 2013.  See http://sourceforge.net/p/glew/bugs/201/
        import re
        fd = open('glew.rc')
        text = re.sub('VALUE "Comments".*$', '', fd.read())
        fd.close()
        fd = open('glew.rc', 'w')
        fd.write(text)
        fd.close()

        self.msbuild(winbrew.msbuild_args+('build\\vc10\\glew_static.vcxproj',))
        self.libs('lib\\Release\\Win32')
        self.includes('include')

    def test(self):
        pass
