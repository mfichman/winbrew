import winbrew
import os

class Llvm(winbrew.Formula):
    url = 'https://github.com/llvm/llvm-project/releases/download/llvmorg-13.0.0/llvm-project-13.0.0.src.tar.xz'
    homepage = 'https://llvm.org'
    sha1 = 'c8ebad168710ede8c281bf81c79ef7e85213e274'
    build_deps = ('cmake',)
    deps = ()

    def build(self):
        path = os.getcwd()
        self.cd('llvm')
        self.cmake_build('../build', winbrew.cmake_args+(
            f'-DLLVM_TARGETS_TO_BUILD=host',
            f'-DLLVM_ENABLE_PROJECTS=clang;clang-tools-extra;lld;lldb',
            f'-DLLVM_ENABLE_PLUGINS=on',
            f'-DLLVM_ENABLE_ASSERTIONS=on',
            f'-DCMAKE_BUILD_TYPE=release',
            f'-DCMAKE_INSTALL_PREFIX={path}/install',
        ))

    def install(self):
        self.cmake(('--install', 'build'))
        self.includes(r'llvm\include')
        self.libs(r'build\Release\lib')
        self.bins(r'build\Release\bin')

    def test(self):
        pass
