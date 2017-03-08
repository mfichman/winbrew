import winbrew
import os
import sys
import subprocess

class Vim(winbrew.Formula):
    url = 'https://github.com/vim/vim/archive/v8.0.0430.zip'
    homepage = 'https://vim.org'
    sha1 = '8702e52daa4122103808f9e628e2d0e4a7127eff'
    build_deps = ()
    deps = (
        'luajit',
    )

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
        self.bin('vimrun.exe')
        self.cd('..')
        self.copy('runtime', 'bin\\vim80')

    def test(self):
        self.system('vim --version')
