import winbrew
import shutil

class Luajit(winbrew.Formula):
    url = 'http://luajit.org/download/LuaJIT-2.0.5.zip'
    homepage = 'http://luajit.org'
    sha1 = '89c5792d5c560c6c73d8b98565422468d100835b'
    build_deps = ()
    deps = ()

    def patch(self):
        self.apply_patch(PATCH_BUILD_STATIC_MD)

    def build(self):
        self.cd('src')
        self.system('msvcbuild.bat static')
        shutil.move('lua51.lib', 'lua51-static.lib')
        self.system('msvcbuild.bat')

    def install(self):
        self.cd('src')

        self.include('lua.hpp', dest='luajit-2.0\\lua.hpp')
        self.include('luajit.h', dest='luajit-2.0\\luajit.h')
        self.include('lua.h', dest='luajit-2.0\\lua.h')
        self.include('lualib.h', dest='luajit-2.0\\lualib.h')
        self.include('lauxlib.h', dest='luajit-2.0\\lauxlib.h')
        self.include('luaconf.h', dest='luajit-2.0\\luaconf.h')

        # For packages that require standard Lua
        self.include('lua.hpp', dest='lua.hpp')
        self.include('luajit.h', dest='luajit.h')
        self.include('lua.h', dest='lua.h')
        self.include('lualib.h', dest='lualib.h')
        self.include('lauxlib.h', dest='lauxlib.h')
        self.include('luaconf.h', dest='luaconf.h')

        luafiles = [
            'bc', 'bcsave', 'dis_arm', 'dis_mips', 'dis_mipsel',
            'dis_ppc', 'dis_x64', 'dis_x86', 'dump', 'v', 'vmdef'
        ]
        for luafile in luafiles:
            src = 'jit\\%s.lua' % luafile
            dst = 'lua\\jit\\%s.lua' % luafile
            self.bin(src, dst)
        self.libs('.')
        self.bin('luajit.exe')

    def test(self):
        self.system('luajit -v')


PATCH_BUILD_STATIC_MD = r"""
--- src\msvcbuild.bat
+++ src\msvcbuild.bat
@@ -76,7 +76,7 @@
 @if errorlevel 1 goto :BAD
 @goto :MTDLL
 :STATIC
-%LJCOMPILE% lj_*.c lib_*.c
+%LJCOMPILE% /MD lj_*.c lib_*.c
 @if errorlevel 1 goto :BAD
 %LJLIB% /OUT:%LJLIBNAME% lj_*.obj lib_*.obj
 @if errorlevel 1 goto :BAD
@@ -90,7 +90,7 @@
 if exist %LJDLLNAME%.manifest^
   %LJMT% -manifest %LJDLLNAME%.manifest -outputresource:%LJDLLNAME%;2

-%LJCOMPILE% luajit.c
+%LJCOMPILE% /MD luajit.c
 @if errorlevel 1 goto :BAD
 %LJLINK% /out:luajit.exe luajit.obj %LJLIBNAME%
 @if errorlevel 1 goto :BAD
"""
