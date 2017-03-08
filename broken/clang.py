
import winbrew

class Clang(winbrew.Formula):
    url = 'https://github.com/llvm-mirror/clang/archive/release_39.zip'
    homepage = 'https://clang.llvm.org'
    sha1 = 'a9de8f48c0d9d4d55b8500cf4781ccbbcaac75bc'
    build_deps = ()
    deps = ()

    def install(self):
        self.cmake_build('build')

    def test(self):
        pass
