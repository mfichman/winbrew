
import winbrew

class Sqlite(winbrew.Formula):
    url = 'http://www.sqlite.org/2014/sqlite-amalgamation-3080600.zip'
    homepage = ''
    sha1 = '6f6ab5ee38eed46ee0d9a8cd8f1e13f94bba99b3'
    build_deps = ()
    deps = ()

    def install(self):
        self.system('cl /c /O2 sqlite3.c shell.c')
        self.system('lib /out:sqlite3.lib sqlite3.obj')
        self.system('link /out:sqlite3.exe sqlite3.lib shell.obj')
        self.lib('sqlite3.lib')
        self.bin('sqlite3.exe') 

    def test(self):
        pass
