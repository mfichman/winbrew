import os

# Default paths for libraries, header files, binaries, etc.
home = os.environ.get('WINBREW_HOME', 'C:\\WinBrew')
formula_path = os.path.join(home, 'formula')
lib_path = os.path.join(home, 'lib')
include_path = os.path.join(home, 'include')
bin_path = os.path.join(home, 'bin')
cache_path = os.path.join(home, 'cache')
manifest_path = os.path.join(home, 'manifest')

formula_url = 'https://github.com/mfichman/winbrew.git'
