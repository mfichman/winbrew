import winbrewtest
import subprocess
import shlex
import os
import shutil

class CliTest(winbrewtest.TestCase):

    def check_command(self, cmd, expected=None):
        if expected:
            output = subprocess.check_output(['winbrew']+shlex.split(cmd))
            assert expected == output
        else:
            subprocess.check_call(['winbrew']+shlex.split(cmd))

    def test_update(self):
        self.check_command('update')

    def test_help(self):
        self.check_command('-h')

    def test_create(self):
        os.environ['EDITOR'] = 'echo'
        path = os.path.join(self.winbrew_home, 'formula', 'NewPkg.py')
        self.check_command('create NewPkg', path+'\n')
        assert(os.path.isfile(path))

    def test_edit(self):
        os.environ['EDITOR'] = 'echo'
        path = os.path.join(self.winbrew_home, 'formula', 'NewPkg.py')
        self.check_command('edit NewPkg', path+'\n')

    def test_install(self):
        self.check_command('install cmake') 
        assert(os.path.isfile(os.path.join(self.winbrew_home, 'bin', 'cmake.exe')))

    def test_freeze(self):
        self.check_command('install cmake') 
        self.check_command('freeze', 'cmake\n')

    def test_uninstall(self):
        self.check_command('install cmake') 
        self.check_command('uninstall cmake')
        assert(not os.path.exists(os.path.join(self.winbrew_home, 'bin', 'cmake.exe')))

    def test_test(self):
        self.check_command('test cmake')

    def test_download(self):
        path = os.path.join(self.winbrew_home, 'cache', 'cmake')
        if os.path.exists(path):
            shutil.rmtree(path)  
        self.check_command('uninstall cmake')
        self.check_command('download cmake')
        assert(os.path.exists(path))

