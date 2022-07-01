
import winbrew

class K3Sup(winbrew.Formula):
    url = 'https://github.com/alexellis/k3sup/releases/download/0.11.1/k3sup.exe'
    homepage = 'https://github.com/alexellis/k3sup'
    sha1 = 'd4c9f03deb1a1e587f54626ed7b44b466586bfa8'
    build_deps = ()
    deps = ()

    def build(self):
        pass

    def install(self):
        self.bin('k3sup','k3sup.exe')

    def test(self):
        pass
