import winbrew
import shutil

class Luajit(winbrew.Formula):
    url = 'https://luajit.org/git/luajit.git'
    homepage = 'https://luajit.org'
    sha1 = 'd492cc10a77c5b8aa626e06a85ca432117a95a23'

    build_deps = ()
    deps = ()

    def patch(self):
        self.apply_patch(PATCH_BUILD_STATIC_MD)

    def build(self):
        self.system('git checkout v2.1')
        self.cd('src')
        self.system('msvcbuild.bat static')
        shutil.move('lua51.lib', 'lua51-static.lib')
        self.system('msvcbuild.bat')

    def install(self):
        self.cd('src')

        self.include('lua.hpp', dest='luajit-2.1\\lua.hpp')
        self.include('luajit.h', dest='luajit-2.1\\luajit.h')
        self.include('lua.h', dest='luajit-2.1\\lua.h')
        self.include('lualib.h', dest='luajit-2.1\\lualib.h')
        self.include('lauxlib.h', dest='luajit-2.1\\lauxlib.h')

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
        self.bin('lua51.dll')

    def test(self):
        self.system('luajit -v')


PATCH_BUILD_STATIC_MD = r"""
--- src\msvcbuild.bat
+++ src\msvcbuild.bat
@@ -17,7 +17,7 @@
 @setlocal
 @rem Add more debug flags here, e.g. DEBUGCFLAGS=/DLUA_USE_ASSERT
 @set DEBUGCFLAGS=
-@set LJCOMPILE=cl /nologo /c /O2 /W3 /D_CRT_SECURE_NO_DEPRECATE /D_CRT_STDIO_INLINE=__declspec(dllexport)__inline
+@set LJCOMPILE=cl /nologo /c /O2 /W3 /D_CRT_SECURE_NO_DEPRECATE /D_CRT_STDIO_INLINE=__declspec(dllexport)__inline /MD
 @set LJDYNBUILD=/DLUA_BUILD_AS_DLL /MD
 @set LJDYNBUILD_DEBUG=/DLUA_BUILD_AS_DLL /MDd 
 @set LJCOMPILETARGET=/Zi
 """
