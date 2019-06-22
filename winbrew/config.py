import os

# Default paths for libraries, header files, binaries, etc.
home = os.environ.get('WINBREW_HOME', os.path.join(os.environ['LOCALAPPDATA'], 'WinBrew'))
formula_path = os.environ.get('WINBREW_PATH', os.path.join(home, 'formula'))
lib_path = os.path.join(home, 'lib')
include_path = os.path.join(home, 'include')
bin_path = os.path.join(home, 'bin')
cache_path = os.path.join(home, 'cache')
manifest_path = os.path.join(home, 'manifest')
formula_url = 'https://github.com/mfichman/winbrew.git'
sdk_path = r'C:\Program Files\Microsoft SDKs\Windows\v7.1'
sdk_include_path = os.path.join(sdk_path, 'Include')
sdk_lib_path = os.path.join(sdk_path, 'Lib', 'x64')
sdk_bin_path = os.path.join(sdk_path, 'Bin', 'x64')
env = os.environ.copy()
