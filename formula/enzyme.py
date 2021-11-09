
import winbrew

class Enzyme(winbrew.Formula):
    url = 'https://github.com/wsmoses/Enzyme.git'
    homepage = 'https://enzyme.mit.edu'
    sha1 = 'a48d7fa3741ab76d492b3550d6074d72fb49798a'
    build_deps = ('cmake', 'llvm', 'ninja')
    deps = ()

    def build(self):
        cache_path = winbrew.cache_path.replace('\\', '/')
        llvm_path = f'{cache_path}/llvm/llvm-project-11.0.0/install'

        self.mkdir('build')
        self.cd('enzyme')
        self.cmake(('-G', 'Ninja', '-B', '../build',
            #f'-DCMAKE_C_COMPILER={llvm_path}/bin/clang.exe',
            #f'-DCMAKE_CXX_COMPILER={llvm_path}/bin/clang++.exe',
            f'-DCMAKE_C_COMPILER=cl.exe',
            f'-DCMAKE_CXX_COMPILER=cl.exe',
            #f'-DCMAKE_CXX_FLAGS=-frtti',
            f'-DLLVM_DIR={llvm_path}/lib/cmake/llvm',
        ))
        self.cmake(('--build', '../build'))

    def install(self):
        raise

    def test(self):
        pass
