import winbrewtest
import glob
import os
import subprocess

class FormulaTest(winbrewtest.TestCase):
    # This test installs all the packages! May take a while to run.

    def test_install(self):
        packages = glob.glob(os.path.join(self.winbrew_path, '*.py'))
        packages = [os.path.splitext(os.path.split(n)[1])[0] for n in packages]
        subprocess.check_call(['winbrew', 'update'])
        subprocess.check_call(['winbrew', 'install']+packages, shell=True)


FormulaTest().test_install()

