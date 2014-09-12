import winbrew
import os
import glob

class Sdl2(winbrew.Formula):
    url = 'http://libsdl.org/release/SDL2-2.0.3.zip'
    homepage = 'http://libsdl.org'
    sha1 = '9283f1ce25b8f3155b6960b214cb6a706c285e27'
    build_deps = ()
    deps = ()

    def directx(self):
        """
        Find the DirectX SDK and set the INCLUDE/LIBPATH env vars to include
        the path to the header/library files.
        """
        sdks = glob.glob("C:\\Program Files*\\Microsoft DirectX SDK*")
        try:
            sdk = sdks[0]
        except IndexError, e:
            self.error("no DirectX SDK found")
        os.environ['LIBPATH'] = ';'.join((
            os.environ.get('LIBPATH', ''),
            os.path.join(sdk, 'Lib', 'x86'),
        ))
        os.environ['INCLUDE'] = ';'.join((
            os.environ.get('INCLUDE', ''),
            os.path.join(sdk, 'Include')
        ))

    def install(self):
        self.directx()
        self.cd('VisualC')
        self.msbuild(winbrew.msbuild_args+(
            '/p:VCBuildAdditionalOptions=/useenv', 
            '/p:VCBuildAdditionalOptions=/arch:SSE2',
            'SDL_VS2010.sln'))
        self.includes('include', 'SDL2')

    def test(self):
        pass
