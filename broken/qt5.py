import winbrew
import os

class Qt5(winbrew.Formula):
    url = 'https://github.com/qt/qt5.git'
    #tag = 'v5.9.0-alpha1'
    homepage = 'https://www.qt.io'
    sha1 = '020954eb0240fa18e488afb8adc3e948b0e08907'
    build_deps = ()
    deps = ()

    def build(self):
        os.environ.update({
            'QTMAKESPEC': 'win32-msvc2017',
            'PATH': os.pathsep.join((
                '{0}\\qt5\\qtbase\\bin'.format(os.getcwd()),
                '{0}\\qt5\\gnuwin32\\bin'.format(os.getcwd()),
                '{0}\\qt5\\qtrepotools\\bin'.format(os.getcwd()),
                os.environ['PATH'],
            )),
        })
        self.system('configure.bat -nomake examples -opensource')
        self.nmake()

    def test(self):
        pass
