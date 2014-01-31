import winbrew

class Glew(winbrew.Formula):
    url = 'http://downloads.sourceforge.net/project/glew/glew/1.10.0/glew-1.10.0.zip'
    homepage = 'http://glew.sourceforge.net'
    sha1 = ''
    build_deps = ()
    deps = ()

    def broken_rc_workaround(self)
        # Workaround for broken RC compiler in Visual Studio 2013.  See http://sourceforge.net/p/glew/bugs/201/
        import re
        fd = open('build\\glew.rc')
        text = re.sub('VALUE "Comments".*$', '', fd.read())
        fd.close()
        fd = open('build\\glew.rc', 'w')
        fd.write(text)
        fd.close()

    def install(self):
        self.broken_rc_workaround()
        self.msbuild(winbrew.msbuild_args+('build\\vc10\\glew_static.vcxproj',))
        self.libs('lib\\Release\\Win32')
        self.includes('include')

    def test(self):
        pass
