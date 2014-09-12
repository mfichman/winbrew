import os

class TestCase(object):
    winbrew_home = os.path.join(os.getcwd(), '.winbrewtest')
    os.environ['WINBREW_HOME'] = winbrew_home
