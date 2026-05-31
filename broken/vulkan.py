
import winbrew

class Vulkan(winbrew.Formula):
    url = 'https://sdk.lunarg.com/sdk/download/1.3.239.0/windows/VulkanRT-1.3.239.0-Components.zip'
    homepage = 'https://vulkan.lunarg.com'
    sha1 = '84412d30d5f3eda8fca83523d6baa1ad9186aa99'
    build_deps = ()
    deps = ()

    def build(self):
        pass

    def install(self):
        self.bin('x64\\vulkaninfo.exe')
        self.lib('x64\\vulkan-1.dll')
        self.lib('x64\\vulkan-1.pdb')

    def test(self):
        pass
