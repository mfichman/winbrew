import winbrew
import os

class Glfw(winbrew.Formula):
    url = 'https://github.com/glfw/glfw/releases/download/3.3.5/glfw-3.3.5.zip'
    homepage = 'http://www.glfw.org'
    sha1 = 'dbefa7f7d7edd79718fee8845db0722f04ad1d5c'
    build_deps = ('cmake',)
    deps = ()
    options = {
        'build-examples': 'Build example programs',
        'build-tests': 'Build tests',
        'build-docs': 'Build documentation',
        'shared': 'Build shared libraries',
    }

    def patch(self):
        self.apply_patch(PATCH_GLFW_FLOAT_PIXEL_TYPE)

    def build(self):
        self.cmake_build('build', winbrew.cmake_args+(
            '-DBUILD_SHARED_LIBS=%s' % ('ON' if self.option('shared') else 'OFF'),
            '-DGLFW_BUILD_EXAMPLES=%s' % ('ON' if self.option('build-examples') else 'OFF'),
            '-DGLFW_BUILD_TESTS=%s' % ('ON' if self.option('build-tests') else 'OFF'),
            '-DGLFW_BUILD_DOCS=%s' % ('ON' if self.option('build-docs') else 'OFF'),
        ))

    def install(self):
        self.includes('include\\GLFW', 'GLFW')
        self.lib('build\\src\\Release\\glfw3.lib', 'glfw.lib')


PATCH_GLFW_FLOAT_PIXEL_TYPE = """
diff --git a/include/GLFW/glfw3.h b/include/GLFW/glfw3.h
index a33c5645..665c1b75 100644
--- a/include/GLFW/glfw3.h
+++ b/include/GLFW/glfw3.h
@@ -942,6 +942,12 @@ extern "C" {
  */
 #define GLFW_DOUBLEBUFFER           0x00021010

+/*! @brief Framebuffer pixel format float type hint.
+  *
+  *  Framebuffer pixel format float type [hint](@ref GLFW_FLOAT_PIXEL_TYPE).
+  */
+#define GLFW_FLOAT_PIXEL_TYPE       0x00021011
+
 /*! @brief Context client API hint and attribute.
  *
  *  Context client API [hint](@ref GLFW_CLIENT_API_hint) and
diff --git a/src/internal.h b/src/internal.h
index ad619b4e..72b666da 100644
--- a/src/internal.h
+++ b/src/internal.h
@@ -327,6 +327,7 @@ struct _GLFWfbconfig
     GLFWbool    sRGB;
     GLFWbool    doublebuffer;
     GLFWbool    transparent;
+    GLFWbool    floatPixelType;
     uintptr_t   handle;
 };

diff --git a/src/wgl_context.c b/src/wgl_context.c
index 72ad11de..1c5d887b 100644
--- a/src/wgl_context.c
+++ b/src/wgl_context.c
@@ -186,6 +186,9 @@ static int choosePixelFormat(_GLFWwindow* window,
             if (findAttribValue(WGL_STEREO_ARB))
                 u->stereo = GLFW_TRUE;

+            if (findAttribValue(WGL_PIXEL_TYPE_ARB) == WGL_TYPE_RGBA_FLOAT_ARB)
+                u->floatPixelType = GLFW_TRUE;
+
             if (_glfw.wgl.ARB_multisample)
                 u->samples = findAttribValue(WGL_SAMPLES_ARB);

diff --git a/src/wgl_context.h b/src/wgl_context.h
index 47f04592..6204e6aa 100644
--- a/src/wgl_context.h
+++ b/src/wgl_context.h
@@ -30,6 +30,7 @@
 #define WGL_DRAW_TO_WINDOW_ARB 0x2001
 #define WGL_PIXEL_TYPE_ARB 0x2013
 #define WGL_TYPE_RGBA_ARB 0x202b
+#define WGL_TYPE_RGBA_FLOAT_ARB 0x21A0
 #define WGL_ACCELERATION_ARB 0x2003
 #define WGL_NO_ACCELERATION_ARB 0x2025
 #define WGL_RED_BITS_ARB 0x2015
diff --git a/src/window.c b/src/window.c
index b87a2609..b97e51a7 100644
--- a/src/window.c
+++ b/src/window.c
@@ -341,6 +341,9 @@ GLFWAPI void glfwWindowHint(int hint, int value)
         case GLFW_SRGB_CAPABLE:
             _glfw.hints.framebuffer.sRGB = value ? GLFW_TRUE : GLFW_FALSE;
             return;
+        case GLFW_FLOAT_PIXEL_TYPE:
+            _glfw.hints.framebuffer.floatPixelType = value ? GLFW_TRUE : GLFW_FALSE;
+            return;
         case GLFW_RESIZABLE:
             _glfw.hints.window.resizable = value ? GLFW_TRUE : GLFW_FALSE;
             return;
"""
