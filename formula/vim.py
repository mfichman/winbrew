import winbrew
import os
import sys
import subprocess

class Vim(winbrew.Formula):
    url = 'https://github.com/vim/vim/archive/v8.1.1124.zip'
    homepage = 'https://vim.org'
    sha1 = '0cda0593d1ae6348410fb6370976c07103322c50'
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

    def build(self):
        os.environ['SDK_INCLUDE_DIR'] = os.path.join(winbrew.config.sdk_path, 'include')
        os.environ['INCLUDE'] = ';'.join((
            os.environ['INCLUDE'],
            os.path.join(winbrew.config.include_path, 'luajit'),
        ))

        vim_path = os.path.join(winbrew.config.home, 'bin\\vim81')

        self.cd('src')
        self.nmake(('-f', 'Make_mvc.mak',
            'GUI=%s' % ('no' if self.option('disable-gui') else 'yes'),
            'LUA=%s' % ('no' if self.option('disable-lua') else winbrew.config.home),
            'LUA_VER=51',
            'DYNAMIC_LUA=yes',
            'PYTHON3=%s' % ('no' if self.option('disable-python') else sys.prefix),
            'PYTHON3_VER=35',
            'DYNAMIC_PYTHON3=yes',
            'VIMRUNTIMEDIR=%s' % vim_path,
        ))

    def install(self):
        self.bin('src\\gvim.exe')
        self.bin('src\\vimrun.exe')
        self.copy('runtime', 'bin\\vim81')

    def test(self):
        self.system('vim --version')
