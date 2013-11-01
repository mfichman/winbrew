from setuptools import setup

setup(
    name = 'winbrew',
    version = '0.0.1',
    author = 'Matt Fichman',
    author_email = 'matt.fichman@gmail.com',
    description = ('Package installer for Windows'),
    license = 'MIT',
    keywords = ('installer', 'windows', 'package'),
    url = 'http://github.com/mfichman/winbrew',
    packages = ['winbrew', 'winbrew.formulas'],
    entry_points = {
        'console_scripts': (
            'winbrew = winbrew.execute:main'
        )
    }
)
    
    
    
    
