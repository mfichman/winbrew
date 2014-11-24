import winbrew

class Glew(winbrew.Formula):
    url = 'http://downloads.sourceforge.net/project/glew/glew/1.10.0/glew-1.10.0.zip'
    homepage = 'http://glew.sourceforge.net'
    sha1 = 'da45a883ca9b2a8e8fc1a642bd043f251ad69151'
    build_deps = ()
    deps = ()

    def broken_rc_workaround(self):
        # Workaround for broken RC compiler in Visual Studio 2013.  See http://sourceforge.net/p/glew/bugs/201/
        import re
        fd = open('build\\glew.rc')
        text = re.sub('VALUE "Comments".*', '', fd.read())
        fd.close()
        fd = open('build\\glew.rc', 'w')
        fd.write(text)
        fd.close()

    def multi_threaded_dll_workaround(self):
        fd = open('build\\vc10\\glew_static.vcxproj')
        output = fd.read().replace(
            '<RuntimeLibrary>MultiThreaded</RuntimeLibrary>', 
            '<RuntimeLibrary>MultiThreadedDll</RuntimeLibrary>')
        fd = open('build\\vc10\\glew_static.vcxproj', 'w')
        fd.write(output)
        fd.close()

    def install(self):
        self.broken_rc_workaround()
        self.multi_threaded_dll_workaround()
        
        self.msbuild(winbrew.msbuild_args+('build\\vc10\\glew_static.vcxproj','/p:Configuration=Release'))
        self.msbuild(winbrew.msbuild_args+('build\\vc10\\glew_shared.vcxproj','/p:Configuration=Release'))

        self.lib('lib\\Release\\Win32\\glew32s.lib', 'glew.lib')
        self.lib('bin\\Release\\Win32\\glew32.dll', 'glew.dll')
        self.includes('include')

    def test(self):
        pass
