import winbrew
import winbrew.util
import shutil
import os
import re

class Freetype2(winbrew.Formula):
    url = 'https://download.savannah.gnu.org/releases/freetype/freetype-2.14.3.tar.xz'
    homepage = 'http://freetype.org'
    sha1 = '62e26b89a057ad4f1e28af977945d5c1975a8e67'
    build_deps = ('cmake',)
    deps = ()

    def build(self):
        # Set the FT_EXPORT and FT_BASE macros for dll-mode so that symbols are
        # exported by the DLL.
        ftoption = 'include\\freetype\\config\\ftoption.h'
        ftoption_orig = ftoption + '.orig'
        if not os.path.exists(ftoption_orig):
            shutil.copyfile(ftoption, ftoption_orig)
        with open(ftoption_orig) as infile, open(ftoption, 'w') as outfile:
            for line in infile:
                if re.search('#define FT_EXPORT\(',line):
                    outfile.write('#ifndef FREETYPE_STATIC\n')
                    outfile.write('#ifdef FT2_BUILD_LIBRARY\n')
                    outfile.write('#define FT_EXPORT(x) __declspec(dllexport) x\n')
                    outfile.write('#else\n')
                    outfile.write('#define FT_EXPORT(x) __declspec(dllimport) x\n')
                    outfile.write('#endif\n')
                    outfile.write('#endif\n')
                elif re.search('#define FT_EXPORT_DEF\(',line):
                    outfile.write('#ifndef FREETYPE_STATIC\n')
                    outfile.write('#ifdef FT2_BUILD_LIBRARY\n')
                    outfile.write('#define FT_EXPORT_DEF(x) __declspec(dllexport) x\n')
                    outfile.write('#endif\n')
                    outfile.write('#endif\n')
                    pass
                else:
                    outfile.write(line)

        self.cmake_build('build', winbrew.cmake_args+(
            '-DCMAKE_C_FLAGS="-D_CRT_SECURE_NO_WARNINGS -DFREETYPE_STATIC"',
            '-DBUILD_SHARED_LIBS=OFF',
        ))
        shutil.move('build\\Release\\freetype.lib','build\\Release\\freetype-static.lib')
        self.cmake_build('build', winbrew.cmake_args+(
            '-DCMAKE_C_FLAGS="-D_CRT_SECURE_NO_WARNINGS"',
            '-DBUILD_SHARED_LIBS=ON',
        ))

    def install(self):
        self.lib('build\\Release\\freetype-static.lib')
        self.lib('build\\Release\\freetype.dll')
        self.lib('build\\Release\\freetype.lib')
        self.includes('include\\freetype','freetype')

    def test(self):
        pass

