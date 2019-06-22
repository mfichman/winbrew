
import winbrew

class Flac(winbrew.Formula):
    url = 'https://github.com/xiph/flac/archive/1.3.1.zip'
    homepage = 'https://xiph.org/flac'
    sha1 = '242014d22b53114e80c509081cfdf8cc4af4f0ed'
    build_deps = ('cmake','ogg')
    deps = ('ogg',)

    def build(self):
        self.patch(PATCH_WIN_UTF8_IO)
        self.msbuild(args=(r'src\libFLAC\libFLAC_static.vcxproj',)+winbrew.formula.msbuild_args)

    def install(self):
        self.lib(r'src\libFLAC\objs\x64\Release\lib\libFLAC_static.lib', dest='flac.lib')
        self.includes(r'include\FLAC', dest='FLAC')

    def test(self):
        pass

PATCH_WIN_UTF8_IO = r"""
--- src\libFLAC\libFLAC_static.vcxproj
+++ src\libFLAC\libFLAC_static.vcxproj
@@ -198,6 +198,7 @@
     <ClCompile Include="ogg_encoder_aspect.c" />
     <ClCompile Include="ogg_helper.c" />
     <ClCompile Include="ogg_mapping.c" />
+    <ClCompile Include="..\share\win_utf8_io\win_utf8_io.c" />
     <ClCompile Include="stream_decoder.c" />
     <ClCompile Include="stream_encoder.c" />
     <ClCompile Include="stream_encoder_framing.c" />
"""
