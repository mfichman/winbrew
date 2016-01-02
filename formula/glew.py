import winbrew

class Glew(winbrew.Formula):
    url = 'http://downloads.sourceforge.net/project/glew/glew/1.13.0/glew-1.13.0.zip'
    homepage = 'http://glew.sourceforge.net'
    sha1 = 'e68946a4f56a10e19f6012662c7734eefd148df3'
    build_deps = ()
    deps = ()

    def install(self):
        self.patch(PATCH_MULTITHREADED_DLL)
        self.msbuild(winbrew.msbuild_args+('build\\vc12\\glew_static.vcxproj','/p:Configuration=Release'))
        self.msbuild(winbrew.msbuild_args+('build\\vc12\\glew_shared.vcxproj','/p:Configuration=Release'))

        self.lib('lib\\Release\\x64\\glew32s.lib', 'glew.lib')
        self.lib('bin\\Release\\x64\\glew32.dll', 'glew.dll')
        self.includes('include')

    def test(self):
        pass

PATCH_MULTITHREADED_DLL = r"""
--- build\vc12\glew_static.vcxproj
+++ build\vc12\glew_static.vcxproj
@@ -228,7 +228,7 @@
   </ItemDefinitionGroup>
   <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='Release|Win32'">
     <ClCompile>
-      <RuntimeLibrary>MultiThreaded</RuntimeLibrary>
+      <RuntimeLibrary>MultiThreadedDll</RuntimeLibrary>
       <InlineFunctionExpansion>OnlyExplicitInline</InlineFunctionExpansion>
       <StringPooling>true</StringPooling>
       <FunctionLevelLinking>true</FunctionLevelLinking>
@@ -253,7 +253,7 @@
   </ItemDefinitionGroup>
   <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='Release|x64'">
     <ClCompile>
-      <RuntimeLibrary>MultiThreaded</RuntimeLibrary>
+      <RuntimeLibrary>MultiThreadedDll</RuntimeLibrary>
       <InlineFunctionExpansion>OnlyExplicitInline</InlineFunctionExpansion>
       <StringPooling>true</StringPooling>
       <FunctionLevelLinking>true</FunctionLevelLinking>
@@ -278,7 +278,7 @@
   </ItemDefinitionGroup>
   <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='Release MX|Win32'">
     <ClCompile>
-      <RuntimeLibrary>MultiThreaded</RuntimeLibrary>
+      <RuntimeLibrary>MultiThreadedDll</RuntimeLibrary>
       <InlineFunctionExpansion>OnlyExplicitInline</InlineFunctionExpansion>
       <StringPooling>true</StringPooling>
       <FunctionLevelLinking>true</FunctionLevelLinking>
@@ -303,7 +303,7 @@
   </ItemDefinitionGroup>
   <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='Release MX|x64'">
     <ClCompile>
-      <RuntimeLibrary>MultiThreaded</RuntimeLibrary>
+      <RuntimeLibrary>MultiThreadedDll</RuntimeLibrary>
       <InlineFunctionExpansion>OnlyExplicitInline</InlineFunctionExpansion>
       <StringPooling>true</StringPooling>
       <FunctionLevelLinking>true</FunctionLevelLinking>
@@ -397,4 +397,4 @@
   <Import Project="$(VCTargetsPath)\Microsoft.Cpp.targets" />
   <ImportGroup Label="ExtensionTargets">
   </ImportGroup>
-</Project>
\ No newline at end of file
+</Project>
    """

