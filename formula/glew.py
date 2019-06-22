import winbrew

class Glew(winbrew.Formula):
    url = 'https://github.com/nigels-com/glew/releases/download/glew-2.1.0/glew-2.1.0.zip'
    homepage = 'https://github.com/nigels-com/glew'
    sha1 = '85ea9f4d1279b107019e48b9174c34e86c634830'
    build_deps = ()
    deps = ()

    def patch(self):
        self.apply_patch(PATCH_MULTITHREADED_DLL)

    def build(self):
        self.msbuild(winbrew.msbuild_args+('build\\vc12\\glew_static.vcxproj','/p:Configuration=Release'))
        self.msbuild(winbrew.msbuild_args+('build\\vc12\\glew_shared.vcxproj','/p:Configuration=Release'))

    def install(self):
        self.lib('lib\\Release\\x64\\glew32s.lib', 'glew.lib')
        self.lib('bin\\Release\\x64\\glew32.dll', 'glew.dll')
        self.includes('include')

    def test(self):
        pass

PATCH_MULTITHREADED_DLL = r"""
--- build\vc12\glew_static.vcxproj
+++ build\vc12\glew_static.vcxproj
@@ -106,7 +106,7 @@
   </PropertyGroup>
   <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='Release|Win32'">
     <ClCompile>
-      <RuntimeLibrary>MultiThreaded</RuntimeLibrary>
+      <RuntimeLibrary>MultiThreadedDll</RuntimeLibrary>
       <InlineFunctionExpansion>OnlyExplicitInline</InlineFunctionExpansion>
       <StringPooling>true</StringPooling>
       <FunctionLevelLinking>true</FunctionLevelLinking>
@@ -132,7 +132,7 @@
   </ItemDefinitionGroup>
   <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='Release|x64'">
     <ClCompile>
-      <RuntimeLibrary>MultiThreaded</RuntimeLibrary>
+      <RuntimeLibrary>MultiThreadedDll</RuntimeLibrary>
       <InlineFunctionExpansion>OnlyExplicitInline</InlineFunctionExpansion>
       <StringPooling>true</StringPooling>
       <FunctionLevelLinking>true</FunctionLevelLinking>
@@ -229,4 +229,4 @@
   <Import Project="$(VCTargetsPath)\Microsoft.Cpp.targets" />
   <ImportGroup Label="ExtensionTargets">
   </ImportGroup>
-</Project>
+</Project>
"""

