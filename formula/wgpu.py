
import winbrew

class Wgpu(winbrew.Formula):
    url = 'https://github.com/gfx-rs/wgpu-native.git'
    homepage = 'https://github.com/gfx-rs/wgpu'
    sha1 = '772d64d2ebea84253bde8ddf4f7d3f265d852849'
    build_deps = ('make',)
    deps = ()

    def build(self):
        self.system('git submodule update --init')
        self.system('make lib-native-release')
        self.system('git submodule update --init')

    def install(self):
        self.lib(r'..\wgpu-build\target\release\wgpu_native.lib')
        self.lib(r'..\wgpu-build\target\release\wgpu_native.dll')
        self.include(r'..\wgpu-build\ffi\webgpu-headers\webgpu.h')
        self.include(r'..\wgpu-build\ffi\wgpu.h')

    def test(self):
        pass
