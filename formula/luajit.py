import winbrew

class Luajit(winbrew.Formula):
    url = 'http://luajit.org/download/LuaJIT-2.0.3.zip'
    homepage = 'http://luajit.org'
    sha1 = 'de92685a7d59210be14a409b1596ea0bece15cfe'
    build_deps = ()
    deps = ()

    def install(self):
        self.cd('src')
        self.system('msvcbuild.bat')
        self.include('lua.hpp', dest='luajit-2.0\\lua.hpp')
        self.include('luajit.h', dest='luajit-2.0\\luajit.h')
        self.include('lua.h', dest='luajit-2.0\\lua.h')
        self.include('lualib.h', dest='luajit-2.0\\lualib.h')
        self.include('lauxlib.h', dest='luajit-2.0\\lauxlib.h')
        self.include('luaconf.h', dest='luajit-2.0\\luaconf.h')

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
