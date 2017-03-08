
import winbrew
import os

class Ruby(winbrew.Formula):
    url = 'https://cache.ruby-lang.org/pub/ruby/2.3/ruby-2.3.3.tar.gz'
    homepage = 'https://www.ruby-lang.org'
    sha1 = '1014ee699071aa2ddd501907d18cbe15399c997d'
    build_deps = ()
    deps = ()

    def install(self):
        self.patch(PATCH_WIN32_PIOINFO)
        self.mkdir('bld')
        self.cd('bld')
        self.system(r'..\\win32\\configure.bat --target=x64-mswin64 --prefix=.\\install', shell=True)
        self.nmake()
        self.nmake(('install',))
        self.bin(r'install\bin\erb.cmd')
        self.bin(r'install\bin\gem.cmd')
        self.bin(r'install\bin\irb.cmd')
        self.bin(r'install\bin\rake')
        self.bin(r'install\bin\rake.bat')
        self.bin(r'install\bin\ri.cmd')
        self.bin(r'install\bin\ruby.exe')
        self.bin(r'install\bin\rubyw.exe')
        self.includes(r'install\include\ruby-2.3.0', dest=r'ruby-2.3.0')
        self.copy(r'install\lib\ruby', dest=r'lib\ruby')
        self.copy(r'install\share\doc\ruby', dest=r'share\doc\ruby')
        self.copy(r'install\share\ri', dest=r'share\ri')
        self.lib(r'install\bin\x64-vcruntime141-ruby230.dll')
        self.lib(r'install\lib\x64-vcruntime141-ruby230.lib')
        self.lib(r'install\lib\x64-vcruntime141-ruby230-static.lib')

    def test(self):
        pass

PATCH_WIN32_PIOINFO = r"""
--- win32\mkexports.rb
+++ win32\mkexports.rb
@@ -114,6 +114,7 @@ def each_export(objs)
         when /OBJECT/, /LIBRARY/
           next if /^[[:xdigit:]]+ 0+ UNDEF / =~ l
           next unless /External/ =~ l
+          next if /(?:_local_stdio_printf_options|v(f|sn?)printf_l)\Z/ =~ l
           next unless l.sub!(/.*?\s(\(\)\s+)?External\s+\|\s+/, '')
           is_data = !$1
           if noprefix or /^[@_]/ =~ l
--- win32\win32.c
+++ win32\win32.c
@@ -2321,6 +2321,21 @@ typedef struct {
 #endif

 /* License: Ruby's */
+#if RUBY_MSVCRT_VERSION >= 140
+typedef struct {
+    CRITICAL_SECTION           lock;
+    intptr_t                   osfhnd;          // underlying OS file HANDLE
+    __int64                    startpos;        // File position that matches buffer start
+    unsigned char              osfile;          // Attributes of file (e.g., open in text mode?)
+    char      textmode;
+    char _pipe_lookahead;
+
+    uint8_t unicode          : 1; // Was the file opened as unicode?
+    uint8_t utf8translations : 1; // Buffer contains translations other than CRLF
+    uint8_t dbcsBufferUsed   : 1; // Is the dbcsBuffer in use?
+    char    dbcsBuffer;           // Buffer for the lead byte of DBCS when converting from DBCS to Unicode
+} ioinfo;
+#else
 typedef struct	{
     intptr_t osfhnd;	/* underlying OS file HANDLE */
     char osfile;	/* attributes of file (e.g., open in text mode?) */
@@ -2332,16 +2347,21 @@ typedef struct	{
     char pipech2[2];
 #endif
 }	ioinfo;
+#endif

 #if !defined _CRTIMP || defined __MINGW32__
 #undef _CRTIMP
 #define _CRTIMP __declspec(dllimport)
 #endif

+#if RUBY_MSVCRT_VERSION >= 140
+static ioinfo ** __pioinfo = NULL;
+#else
 EXTERN_C _CRTIMP ioinfo * __pioinfo[];
+#endif
 static inline ioinfo* _pioinfo(int);

-#define IOINFO_L2E			5
+#define IOINFO_L2E	(RUBY_MSVCRT_VERSION >= 140 ? 6 : 5)
 #define IOINFO_ARRAY_ELTS	(1 << IOINFO_L2E)
 #define _osfhnd(i)  (_pioinfo(i)->osfhnd)
 #define _osfile(i)  (_pioinfo(i)->osfile)
@@ -2356,6 +2376,34 @@ static size_t pioinfo_extra = 0;	/* workaround for VC++8 SP1 */
 static void
 set_pioinfo_extra(void)
 {
+#if RUBY_MSVCRT_VERSION >= 140
+    // get __pioinfo addr with _isatty
+    HMODULE mod = GetModuleHandle("ucrtbase.dll");
+    char *addr = (char*)GetProcAddress(mod, "_isatty");
+    // _osfile(fh) & FDEV /*0x40*/
+#if _WIN64
+    // lea rdx,[__pioinfo's addr in RIP-relative 32bit addr]
+    addr += 0x25;
+# define OPSIZE 3
+    if (memcmp(addr, "\x48\x8d\x15", OPSIZE)) {
+	fprintf(stderr, "unexpected ucrtbase.dll\n");
+	abort();
+    }
+    addr += OPSIZE;
+    int32_t rel = *(int32_t*)(addr);
+    char *rip = addr + 4;
+    __pioinfo = (ioinfo**)(rip + rel);
+#else
+    // mov eax,dword ptr [eax*4+100EB430h]
+    addr += 0x32;
+# define OPSIZE 3
+    if (memcmp(addr, "\x8B\x04\x85", OPSIZE)) {
+	fprintf(stderr, "unexpected ucrtbase.dll\n");
+	abort();
+    }
+    __pioinfo = (ioinfo**)*(intptr_t*)(addr + OPSIZE);
+#endif
+#else
     int fd;

     fd = _open("NUL", O_RDONLY);
@@ -2370,6 +2418,7 @@ set_pioinfo_extra(void)
 	/* not found, maybe something wrong... */
 	pioinfo_extra = 0;
     }
+#endif
 }
 #else
 #define pioinfo_extra 0
"""
