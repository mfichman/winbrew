
import winbrew

class Sqlite(winbrew.Formula):
    url = 'https://www.sqlite.org/2020/sqlite-amalgamation-3340000.zip'
    homepage = 'https://www.sqlite.org'
    sha1 = '0b664afaea760e5f4e675ac2afc80c1e65090af2'
    build_deps = ()
    deps = ()

    def build(self):
        self.system('cl /c /O2 /MD sqlite3.c shell.c')
        self.system('lib /out:sqlite3.lib sqlite3.obj')
        self.system('link /out:sqlite3.exe sqlite3.lib shell.obj')

    def install(self):
        self.lib('sqlite3.lib')
        self.bin('sqlite3.exe')
        self.include('sqlite3.h')
        self.include('sqlite3ext.h')

    def test(self):
        pass
