import winbrew
import string
import os
import glob

class Jpeg(winbrew.Formula):
    url = 'https://ijg.org/files/jpegsr9d.zip'
    homepage = 'www.ilg.org'
    sha1 = 'ed10aa2b5a0fcfe74f8a6f7611aeb346b06a1f99'
    build_deps = ()
    deps = ()

    def broken_vcxproj_workaround(self):
        # The vcxproj has a BOM mark in it...strip those, so that
        # msbuild doesn't crash
        with open('jpeg.vcxproj', 'rb') as fd:
            data = fd.read().decode('utf-8-sig')

        with open('jpeg.vcxproj', 'w') as fd:
            fd.write(data)

    def patch(self):
        if not os.path.exists('jpeg.sln'):
            self.nmake(('/f', 'makefile.vc', 'setup-v16',))
        self.broken_vcxproj_workaround()
        #self.apply_patch(PATCH_X64_COMPILE)

    def build(self):
        sdks = glob.glob("C:\\Program Files*\\Microsoft SDKs\\Windows\\v*\\Include")
        try:
            sdk = sdks[0]
        except IndexError as e:
            self.error("no Windows SDK found")
        os.environ['INCLUDE'] = ';'.join((sdk, os.environ['INCLUDE']))
        if not os.path.exists('jpeg.sln'):
            self.nmake(('/f', 'makefile.vc', 'setup-v16',))
        self.msbuild(winbrew.msbuild_args+('jpeg.vcxproj',))

    def install(self):
        self.lib('Release\\x64\\jpeg.lib')
        self.includes('.')

    def test(self):
        pass


PATCH_X64_COMPILE = r"""
--- jpeg.vcxproj
+++ jpeg.vcxproj
@@ -1,9 +1,9 @@
 <?xml version="1.0" encoding="utf-8"?>
 <Project DefaultTargets="Build" ToolsVersion="15.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
   <ItemGroup Label="ProjectConfigurations">
-    <ProjectConfiguration Include="Release|Win32">
+    <ProjectConfiguration Include="Release|x64">
       <Configuration>Release</Configuration>
-      <Platform>Win32</Platform>
+      <Platform>x64</Platform>
     </ProjectConfiguration>
   </ItemGroup>
   <ItemGroup>
@@ -72,7 +72,7 @@
     <WindowsTargetPlatformVersion>10.0.16299.0</WindowsTargetPlatformVersion>
   </PropertyGroup>
   <Import Project="$(VCTargetsPath)\Microsoft.Cpp.Default.props" />
-  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Release|Win32'" Label="Configuration">
+  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Release|x64'" Label="Configuration">
     <ConfigurationType>StaticLibrary</ConfigurationType>
     <UseDebugLibraries>false</UseDebugLibraries>
     <WholeProgramOptimization>true</WholeProgramOptimization>
@@ -82,12 +82,12 @@
   <Import Project="$(VCTargetsPath)\Microsoft.Cpp.props" />
   <ImportGroup Label="ExtensionSettings">
   </ImportGroup>
-  <ImportGroup Label="PropertySheets" Condition="'$(Configuration)|$(Platform)'=='Release|Win32'">
+  <ImportGroup Label="PropertySheets" Condition="'$(Configuration)|$(Platform)'=='Release|x64'">
     <Import Project="$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props" Condition="exists('$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props')" Label="LocalAppDataPlatform" />
   </ImportGroup>
   <PropertyGroup Label="UserMacros" />
   <PropertyGroup />
-  <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='Release|Win32'">
+  <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='Release|x64'">
     <ClCompile>
       <WarningLevel>Level3</WarningLevel>
       <PrecompiledHeader>NotUsing</PrecompiledHeader>
@@ -108,4 +108,4 @@
   <Import Project="$(VCTargetsPath)\Microsoft.Cpp.targets" />
   <ImportGroup Label="ExtensionTargets">
   </ImportGroup>
-</Project>
+</Project>
"""
