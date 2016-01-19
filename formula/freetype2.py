import winbrew
import winbrew.util
import shutil
import os
import re

class Freetype2(winbrew.Formula):
    url = 'http://downloads.sourceforge.net/project/freetype/freetype2/2.5.2/freetype-2.5.2.tar.bz2'
    homepage = 'http://freetype.org'
    sha1 = '72731cf405b9f7c0b56d144130a8daafa262b729'
    build_deps = ('cmake',)
    deps = ()

    def install(self):
        # Set the FT_EXPORT and FT_BASE macros for dll-mode so that symbols are
        # exported by the DLL.
        if not os.path.exists('include\\config\\ftoption.h.orig'):
            shutil.copyfile('include\\config\\ftoption.h','include\\config\\ftoption.h.orig')
        with open('include\\config\\ftoption.h.orig') as infile, open('include\\config\\ftoption.h', 'w') as outfile:
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
        self.lib('build\\Release\\freetype.lib','freetype-static.lib')
        self.cmake_build('build', winbrew.cmake_args+(
            '-DCMAKE_C_FLAGS="-D_CRT_SECURE_NO_WARNINGS"',
            '-DBUILD_SHARED_LIBS=ON',
        ))
        self.lib('build\\Release\\freetype.dll')
        self.lib('build\\Release\\freetype.lib')
        self.includes('include','freetype')

    def test(self):
        pass

