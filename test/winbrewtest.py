import os
import subprocess

class TestCase(object):
    winbrew_home = os.path.join(os.getcwd(), '.winbrewtest')
    winbrew_path = os.path.join(os.getcwd(), 'formula')
    os.environ['WINBREW_HOME'] = winbrew_home
    os.environ['WINBREW_PATH'] = winbrew_path
    subprocess.check_call(('winbrew', 'update'), shell=True)
