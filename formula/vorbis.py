
import winbrew

class Vorbis(winbrew.Formula):
    url = 'http://downloads.xiph.org/releases/vorbis/libvorbis-1.3.5.zip'
    homepage = 'https://xiph.org/vorbis'
    sha1 = 'ee2a0014961dd1308206cf8d7c4b98709633fc4a'
    build_deps = ()
    deps = ()

    def install(self):
        self.msbuild(args=('win32\\VS2010\\libvorbis\\libvorbis_static.vcxproj',)+winbrew.formula.msbuild_args)
        self.msbuild(args=('win32\\VS2010\\libvorbisfile\\libvorbisfile_static.vcxproj',)+winbrew.formula.msbuild_args)
        self.lib('win32\\VS2010\\libvorbis\\x64\\Release\\libvorbis_static.lib','vorbis.lib')
        self.lib('win32\\VS2010\\libvorbisfile\\x64\\Release\\libvorbisfile_static.lib','vorbisfile.lib')
        self.includes('include')

    def test(self):
        pass
