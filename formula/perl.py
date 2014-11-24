import winbrew
import os

class Perl(winbrew.Formula):
    url = 'http://strawberryperl.com/download/5.18.4.1/strawberry-perl-5.18.4.1-32bit-portable.zip'
    homepage = 'http://strawberryperl.com'
    sha1 = 'f6118ba24e4430a7ddab1200746725f262117fbf'
    build_deps = ()
    deps = ()

    def install(self):
        fd = open('perl.bat', 'w')
        fd.write('@echo off\n')
        fd.write(os.path.join(winbrew.cache_path, 'perl\\perl\\bin\\perl.exe'))
        fd.write(' %*')
        fd.write('\n')
        fd.close()
        self.bin('perl.bat')

    def test(self):
        self.system('perl -v')

