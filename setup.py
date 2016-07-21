from setuptools import setup

setup(
    name = 'winbrew',
    version = '1.1.7',
    author = 'Matt Fichman',
    author_email = 'matt.fichman@gmail.com',
    description = ('Native package installer for Windows'),
    license = 'MIT',
    keywords = ('installer', 'windows', 'package'),
    url = 'http://github.com/mfichman/winbrew',
    packages = ('winbrew',),
    install_requires = (
        'patch>=1.15,<2',
    ),
    entry_points = {
        'console_scripts': (
            'winbrew = winbrew.execute:main',
            'brew = winbrew.execute:main'
        )
    }
)
