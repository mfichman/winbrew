
import winbrew
import string
import os
import glob

class Jpeg(winbrew.Formula):
    url = 'http://www.ijg.org/files/jpegsrc.v9a.tar.gz'
    homepage = 'www.ilg.org'
    sha1 = 'd65ed6f88d318f7380a3a5f75d578744e732daca'
    build_deps = ()
    deps = ()

    def broken_vcxproj_workaround(self):
        # The vcxproj has unprintable characters in it...strip those, so that
        # msbuild doesn't crash
        fd = open('jpeg.vcxproj')
        data = filter(lambda c: c in string.printable, fd.read())
        fd.close()
        fd = open('jpeg.vcxproj', 'w')
        fd.write(data)
        fd.close()

    def install(self):
        sdks = glob.glob("C:\\Program Files*\\Microsoft SDKs\\Windows\\v*\\Include")
        try:
            sdk = sdks[0]
        except IndexError, e:
            self.error("no Windows SDK found")
        os.environ['INCLUDE'] = ';'.join((sdk,os.environ['INCLUDE']))
        if not os.path.exists('jpeg.sln'):
            self.nmake(('/f', 'makefile.vc', 'setup-v10',))
        self.broken_vcxproj_workaround()
        self.msbuild(winbrew.msbuild_args+('jpeg.sln','/p:Configuration=Release'))
        self.lib('Release\\jpeg.lib')

    def test(self):
        pass
