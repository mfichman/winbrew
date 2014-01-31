import winbrew

class Luajit(winbrew.Formula):
    url = 'http://luajit.org/download/LuaJIT-2.0.2.zip'
    homepage = 'http://luajit.org'
    sha1 = ''
    build_deps = ()
    deps = ()

    def install(self):
        self.cd('LuaJIT-2.0.2\\src')
        self.system('msvcbuild.bat')
        self.include('lua.hpp', dest='luajit\\lua.hpp')
        self.include('luajit.h', dest='luajit\\luajit.h')
        self.include('lua.h', dest='luajit\\lua.h')
        self.include('lualib.h', dest='luajit\\lualib.h')
        self.include('lauxlib.h', dest='luajit\\lauxlib.h')
        self.libs('.')
        self.bin('luajit.exe')
    
    def test(self):
        pass
