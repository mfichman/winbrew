
import winbrew

class Sndfile(winbrew.Formula):
    url = 'http://www.mega-nerd.com/libsndfile/files/libsndfile-1.0.25.tar.gz'
    homepage = 'http://www.mega-nerd.com/libsndfile'
    sha1 = 'e95d9fca57f7ddace9f197071cbcfb92fa16748e'
    build_deps = ()
    deps = ()

    def install(self):
        self.cmake_build('build', winbrew.cmake_args+(
            '-DBUILD_SHARED_LIBS=OFF',
        ))

    def test(self):
        pass
