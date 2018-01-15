import winbrew
import os

class Qt5(winbrew.Formula):
    url = 'https://github.com/qt/qt5.git'
    change = 'v5.9.0-alpha1'
    homepage = 'https://www.qt.io'
    sha1 = 'bfe7e2e9568d93f6f517facde00be5f953fc20cd'
    build_deps = ()
    deps = ()

    def install(self):
        env = os.environ.copy()
        env.update({
            'QTMAKESPEC': 'win32-msvc2017',
            'PATH': os.pathsep.join((
                '{0}\\qt5\\qtbase\\bin'.format(os.getcwd()),
                '{0}\\qt5\\gnuwin32\\bin'.format(os.getcwd()),
                '{0}\\qt5\\qtrepotools\\bin'.format(os.getcwd()),
                os.environ['PATH'],
            )),
        })
        print(env['PATH'])
        self.system('configure.bat -nomake examples -opensource')
        self.nmake(env=env)

    def test(self):
        pass
