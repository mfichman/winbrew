from setuptools import setup

setup(
    name = 'winbrew',
    version = '2.0.2',
    author = 'Matt Fichman',
    author_email = 'matt.fichman@gmail.com',
    description = 'Native package installer for Windows, a la Homebrew',
    license = 'MIT',
    keywords = ['installer', 'windows', 'package'],
    url = 'http://github.com/mfichman/winbrew',
    packages = ['winbrew',],
    install_requires = [
        'patch>=1.16,<2',
    ],
    entry_points = {
        'console_scripts': [
            'winbrew = winbrew.execute:main',
            'brew = winbrew.execute:main'
        ]
    }
)
