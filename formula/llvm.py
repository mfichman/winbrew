import winbrew
import os

class Llvm(winbrew.Formula):
    url = 'https://github.com/llvm/llvm-project/releases/download/llvmorg-16.0.6/llvm-project-16.0.6.src.tar.xz'
    homepage = 'https://llvm.org'
    sha1 = '92eaedd6f1dde08751441afcd0a3d0fbfdf95d42'
    build_deps = ('cmake',)
    deps = ()

    def build(self):
        path = os.getcwd()
        self.cd('llvm')
        self.cmake_build('../build', winbrew.cmake_args+(
            f'-DLLVM_TARGETS_TO_BUILD=host',
            f'-DLLVM_ENABLE_PROJECTS=clang;clang-tools-extra;lld;lldb',
            #f'-DLLVM_ENABLE_RUNTIMES=compiler-rt',
            #f'-DLLVM_DIR={path}/build/lib/cmake',
            #f'-DLLVM_CMAKE_DIR={path}/build/lib/cmake/llvm',
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
