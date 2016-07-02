
import winbrew
import shutil

class Make(winbrew.Formula):
    url = 'http://downloads.sourceforge.net/project/gnuwin32/make/3.81/make-3.81-src.zip'
    homepage = 'http://gnuwin32.sourceforge.net/packages/make.htm'
    sha1 = '5b5b4a700fb422bc8d2eb96b5c4d1a21c368b2c1'
    build_deps = ()
    deps = ()

    def install(self):
        self.cd('src\\make\\3.81\\make-3.81-src')
        shutil.copy('config.h.W32','config.h')
        self.patch(PATCH_JOB_AND_MAKEFILE)
        self.nmake(('/f', 'NMakefile'))
        self.bin('WinRel\\make.exe')

    def test(self):
        pass

PATCH_JOB_AND_MAKEFILE = r"""
--- job.c.orig
+++ job.c
@@ -174,7 +174,7 @@

 #endif	/* Don't have `union wait'.  */

-#ifndef	HAVE_UNISTD_H
+#if    0
 extern int dup2 ();
 extern int execve ();
 extern void _exit ();

--- NMakefile.orig
+++ NMakefile
@@ -27,12 +27,12 @@
 MAKEFILE=NMakefile
 SUBPROC_MAKEFILE=NMakefile

-CFLAGS_any = /nologo /MT /W4 /GX /Zi /YX /I . /I glob /I w32/include /D WIN32 /D WINDOWS32 /D _CONSOLE /D HAVE_CONFIG_H
+CFLAGS_any = /nologo /MT /W4 /GX /Zi /YX /I . /I glob /I w32/include /D WIN32 /D WINDOWS32 /D _CONSOLE /D HAVE_CONFIG_H /MACHINE:x64
 CFLAGS_debug = $(CFLAGS_any) /Od /D DEBUG /D _DEBUG /FR.\WinDebug/ /Fp.\WinDebug/make.pch /Fo.\WinDebug/ /Fd.\WinDebug/make.pdb
 CFLAGS_release = $(CFLAGS_any) /O2 /D NDEBUG /FR.\WinRel/ /Fp.\WinRel/make.pch /Fo.\WinRel/

 LDFLAGS_debug = w32\subproc\WinDebug\subproc.lib /NOLOGO /SUBSYSTEM:console\
-	/INCREMENTAL:no /PDB:WinDebug/make.pdb /MACHINE:I386 \
+	/INCREMENTAL:no /PDB:WinDebug/make.pdb /MACHINE:x64 \
 	/OUT:WinDebug/make.exe /DEBUG
 LDFLAGS_release = w32\subproc\WinRel\subproc.lib /NOLOGO /SUBSYSTEM:console\
-	/INCREMENTAL:no /MACHINE:I386 /OUT:WinRel/make.exe
+	/INCREMENTAL:no /MACHINE:I386 /OUT:WinRel/make.exe /MACHINE:x64

--- w32\\subproc\\NMakefile.orig
+++ w32\\subproc\\NMakefile
@@ -27,7 +27,7 @@
 OUTDIR=.
 MAKEFILE=NMakefile

-CFLAGS_any = /nologo /MT /W4 /GX /Z7 /YX /D WIN32 /D WINDOWS32 /D _WINDOWS  -I. -I../include -I../../
+CFLAGS_any = /nologo /MT /W4 /GX /Z7 /YX /D WIN32 /D WINDOWS32 /D _WINDOWS  -I. -I../include -I../../ /MACHINE:x64
 CFLAGS_debug = $(CFLAGS_any) /Od /D _DEBUG /FR.\WinDebug\ /Fp.\WinDebug\subproc.pch /Fo.\WinDebug/
 CFLAGS_release = $(CFLAGS_any) /O2 /FR.\WinRel\ /Fp.\WinRel\subproc.pch /Fo.\WinRel/

"""
