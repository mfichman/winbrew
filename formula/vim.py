
import winbrew
import os
import sys
import subprocess

class Vim(winbrew.Formula):
    url = 'https://github.com/vim/vim/archive/v7.4.2084.zip'
    homepage = 'https://vim.org'
    sha1 = 'c9bf8dc08a14dcc881f6e3317f7b5ac508443320'
    build_deps = ()
    deps = ()

    options = {
        'disable-gui': 'Disable GUI',
        'disable-lua': 'Disable Lua support',
        'disable-python': 'Disable Python support',
        'disable-ruby': 'Disable Ruby support',
    }

    def _ruby_path(self):
        return os.path.split(os.path.split(subprocess.check_output('where ruby'))[0])[0]

    def install(self):
        os.environ['SDK_INCLUDE_DIR'] = os.path.join(winbrew.config.sdk_path, 'include')
        os.environ['INCLUDE'] = ';'.join((
            os.environ['INCLUDE'],
            os.path.join(winbrew.config.include_path, 'luajit'),
        ))

        vim_path = os.path.join(winbrew.config.home, 'bin\\vim74')

        self.cd('src')
        self.system('msvc2010.bat')
        self.nmake(('-f', 'Make_mvc.mak', 
            'GUI=%s' % ('no' if self.option('disable-gui') else 'yes'),
            'LUA=%s' % ('' if self.option('disable-lua') else winbrew.config.home),
            'LUA_VER=51',
            'DYNAMIC_LUA=yes',
            'PYTHON=%s' % ('' if self.option('disable-python') else sys.prefix),
            'PYTHON_VER=27',
            'DYNAMIC_PYTHON=yes',
            'VIMRUNTIMEDIR=%s' % vim_path,
        ))
        self.bin('gvim.exe')
        self.cd('..')
        self.copy('runtime', 'bin\\vim74')

        

    def test(self):
        self.system('vim --version')
