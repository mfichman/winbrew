
import winbrew

class Sqlite(winbrew.Formula):
    url = 'https://www.sqlite.org/2021/sqlite-amalgamation-3360000.zip'
    homepage = 'https://www.sqlite.org'
    sha1 = '0c049c365896b71b6e291c9a262d2d0fbce7b4e6'
    build_deps = ()
    deps = ()

    def build(self):
        self.system('cl /c /O2 /MD /DSQLITE_ENABLE_JSON1 sqlite3.c shell.c')
        self.system('lib /out:sqlite3.lib sqlite3.obj')
        self.system('link /out:sqlite3.exe sqlite3.lib shell.obj')

    def install(self):
        self.lib('sqlite3.lib')
        self.bin('sqlite3.exe')
        self.include('sqlite3.h')
        self.include('sqlite3ext.h')

    def test(self):
        pass
