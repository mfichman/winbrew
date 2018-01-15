import winbrew
import string
import os
import glob

class Jpeg(winbrew.Formula):
    url = 'http://www.ijg.org/files/jpegsrc.v9a.tar.gz'
    homepage = 'www.ilg.org'
    sha1 = 'd65ed6f88d318f7380a3a5f75d578744e732daca'
    build_deps = ()
    deps = ()

    def broken_vcxproj_workaround(self):
        # The vcxproj has unprintable characters in it...strip those, so that
        # msbuild doesn't crash
        fd = open('jpeg.vcxproj')
        data = [c for c in fd.read() if c in string.printable]
        fd.close()
        fd = open('jpeg.vcxproj', 'w')
        fd.write(data)
        fd.close()

    def install(self):
        sdks = glob.glob("C:\\Program Files*\\Microsoft SDKs\\Windows\\v*\\Include")
        try:
            sdk = sdks[0]
        except IndexError as e:
            self.error("no Windows SDK found")
        os.environ['INCLUDE'] = ';'.join((sdk,os.environ['INCLUDE']))
        if not os.path.exists('jpeg.sln'):
            self.nmake(('/f', 'makefile.vc', 'setup-v10',))
        self.broken_vcxproj_workaround()
        self.patch(PATCH_X64_COMPILE)
        self.msbuild(winbrew.msbuild_args+('jpeg.vcxproj',))
        self.lib('x64\\Release\\jpeg.lib')
        self.includes('.')

    def test(self):
        pass


PATCH_X64_COMPILE = r"""
--- jpeg.vcxproj
+++ jpeg.vcxproj
@@ -1,9 +1,9 @@
 <?xml version="1.0" encoding="utf-8"?>
 <Project DefaultTargets="Build" ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
   <ItemGroup Label="ProjectConfigurations">
-    <ProjectConfiguration Include="Release|Win32">
+    <ProjectConfiguration Include="Release|x64">
       <Configuration>Release</Configuration>
-      <Platform>Win32</Platform>
+      <Platform>x64</Platform>
     </ProjectConfiguration>
   </ItemGroup>
   <ItemGroup>
@@ -63,18 +63,18 @@
     <ClCompile Include="jmemnobs.c" />
     <ClCompile Include="jquant1.c" />
     <ClCompile Include="jquant2.c">
-      <Optimization Condition="'$(Configuration)|$(Platform)'=='Release|Win32'">Disabled</Optimization>
-      <BufferSecurityCheck Condition="'$(Configuration)|$(Platform)'=='Release|Win32'">false</BufferSecurityCheck>
+      <Optimization Condition="'$(Configuration)|$(Platform)'=='Release|x64'">Disabled</Optimization>
+      <BufferSecurityCheck Condition="'$(Configuration)|$(Platform)'=='Release|x64'">false</BufferSecurityCheck>
     </ClCompile>
     <ClCompile Include="jutils.c" />
   </ItemGroup>
   <PropertyGroup Label="Globals">
     <ProjectGuid>{019DBD2A-273D-4BA4-BF86-B5EFE2ED76B1}</ProjectGuid>
-    <Keyword>Win32Proj</Keyword>
+    <Keyword>x64Proj</Keyword>
     <RootNamespace>jpeg</RootNamespace>
   </PropertyGroup>
   <Import Project="$(VCTargetsPath)\Microsoft.Cpp.Default.props" />
-  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Release|Win32'" Label="Configuration">
+  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Release|x64'" Label="Configuration">
     <ConfigurationType>StaticLibrary</ConfigurationType>
     <UseDebugLibraries>false</UseDebugLibraries>
     <WholeProgramOptimization>true</WholeProgramOptimization>
@@ -83,12 +83,12 @@
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
"""
