import winbrew

class Atom(winbrew.Formula):
    url = 'https://github.com/atom/atom/archive/master.zip'
    homepage = 'https://atom.io'
    sha1 = ''
    build_deps = ()
    #build_deps = ('git',)
    #build_deps = ('git',)
    deps = ('nodejs',)
    #deps = ('python', 'nodejs')
    options = {

    }

    def install(self):
        self.system('node script/build')

    def test(self):
        pass

