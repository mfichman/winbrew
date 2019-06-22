import os
import shutil
import winbrew.util
import zipfile
import tarfile
import urllib.request, urllib.parse, urllib.error

class Archive:
    """
    Archive describes the type of package to download. Typically, some kind of
    compressed file (tar, zip) or a git repository.
    """

    @staticmethod
    def create(url, work_dir, package_name):
        ext = os.path.splitext(url)[1]
        name = os.path.split(url)[1]

        if ext == '.zip':
            return ZipArchive(url, work_dir, name)
        elif ext == '.gz':
            return TarArchive(url, work_dir, name, compression='gz')
        elif ext == '.tgz':
            return TarArchive(url, work_dir, name, compression='gz')
        elif ext == '.bz2':
            return TarArchive(url, work_dir, name, compression='bz2')
        elif ext == '.msi':
            return MsiArchive(url, work_dir, name)
        elif ext == '.git':
            return GitArchive(url, work_dir, package_name)
        else:
            raise Exception('unknown archive file type')

    def __init__(self, url, work_dir, name):
        self.url = url

        # Parent working directory in cache
        self.work_dir = work_dir

        # File name
        self.name = name

        # Full downloaded file path
        self.path = os.path.join(work_dir, name)

    def download(self):
        if os.path.exists(self.path): return

        winbrew.util.rm_rf(self.work_dir)
        winbrew.util.mkdir_p(self.work_dir)

        with open(self.path, 'wb') as fd, urllib.request.urlopen(self.url) as stream:
            shutil.copyfileobj(stream, fd)

    def clean(self):
        for fn in os.listdir(self.work_dir):
            if fn != self.name:
                winbrew.util.rm_rf(fn)

class ZipArchive(Archive):
    def __init__(self, url, work_dir, name):
        super(ZipArchive, self).__init__(url, work_dir, name)

    @property
    def unpack_dir(self):
        with self.zipfile() as zf:
            return os.path.commonprefix(zf.namelist())

    def zipfile(self):
        return zipfile.ZipFile(self.path)

    def unpack(self):
        if os.path.exists(self.unpack_dir): return # already extracted
        with self.zipfile() as zf: zf.extractall(self.work_dir)

class TarArchive(Archive):
    def __init__(self, url, work_dir, name, compression='gz'):
        super(TarArchive, self).__init__(url, work_dir, name)

        self.compression = compression

    @property
    def unpack_dir(self):
        with self.tarfile() as tf:
            return os.path.commonprefix(tf.getnames())

    def tarfile(self):
        return tarfile.open(self.path, mode='r:%s' % self.compression)

    def unpack(self):
        if os.path.exists(self.path): return # already extracted
        with self.tarfile() as tf: tf.extractall(self.work_dir)

class MsiArchive(Archive):
    def __init__(self, url, work_dir, name, compression='gz'):
        super(MsiArchive, self).__init__(url, work_dir, name)

    @property
    def unpack_dir(self):
        return '.'

    def unpack(self):
        self.system('msiexec /quiet /i %s' % self.path)

class GitArchive(Archive):
    def __init__(self, url, work_dir, name):
        super(GitArchive, self).__init__(url, work_dir, name)

    @property
    def unpack_dir(self):
        return self.name

    def unpack(self):
        pass

    def download(self):
        winbrew.util.rm_rf(self.work_dir)
        winbrew.util.mkdir_p(self.work_dir)

        if os.path.exists(self.path): return

        subprocess.check_call(('git', 'clone', self.url, self.path))
        if getattr(self, 'tag'):
            subprocess.check_call(('git', 'checkout', tab))

    def clean(self):
        subprocess.check_call(('git', '-C', self.unpack_dir, 'reset', '--hard'))
        subprocess.check_call(('git', '-C', self.unpack_dir, 'clean', '-dxf'))
