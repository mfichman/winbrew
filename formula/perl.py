import winbrew
import os

class Perl(winbrew.Formula):
    url = 'http://strawberryperl.com/download/5.18.4.1/strawberry-perl-5.18.4.1-32bit-portable.zip'
    homepage = 'http://strawberryperl.com'
    sha1 = '8ff44654df738d5750be070d4801d14a7f49541b'
    build_deps = ()
    deps = ()

    def install(self):
        self.bin('portableshell.bat', 'perlshell.bat')

    def test(self):
        self.system('perl -v')
