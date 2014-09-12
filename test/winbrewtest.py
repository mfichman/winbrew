import os
import subprocess

class TestCase(object):
    winbrew_home = os.path.join(os.getcwd(), '.winbrewtest')
    os.environ['WINBREW_HOME'] = winbrew_home
    subprocess.check_call(('winbrew', 'update'), shell=True)
