import winbrew

class Luajit(winbrew.Formula):
    url = 'http://luajit.org/download/LuaJIT-2.0.2.zip'
    homepage = 'http://luajit.org'
    sha1 = 'b7b5fd5c5d2c6aaea43b5b2f2b9f2646ddda1568'
    build_deps = ()
    deps = ()

    def install(self):
        self.cd('src')
        self.system('msvcbuild.bat')
        self.include('lua.hpp', dest='luajit\\lua.hpp')
        self.include('luajit.h', dest='luajit\\luajit.h')
        self.include('lua.h', dest='luajit\\lua.h')
        self.include('lualib.h', dest='luajit\\lualib.h')
        self.include('lauxlib.h', dest='luajit\\lauxlib.h')
        self.include('luaconf.h', dest='luajit\\luaconf.h')

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
