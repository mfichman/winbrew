import os
import shutil
import winbrew.util
import zipfile
import tarfile
import urllib
import subprocess

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
        elif ext == '.xz':
            return TarArchive(url, work_dir, name, compression='xz')
        elif ext == '.msi':
            return MsiArchive(url, work_dir, name)
        elif ext == '.git':
            return GitArchive(url, work_dir, package_name)
        elif ext == '.exe':
            return ExeArchive(url, work_dir, package_name)
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
        winbrew.util.rm_rf(self.work_dir)
        winbrew.util.mkdir_p(self.work_dir)

        with open(self.path, 'wb') as fd, self.urlopen() as stream:
            shutil.copyfileobj(stream, fd)

    def urlopen(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
        }

        request = urllib.request.Request(self.url, headers=headers)
        return urllib.request.urlopen(request)

    def clean(self):
        for fn in os.listdir(self.work_dir):
            if fn != self.name:
                winbrew.util.rm_rf(os.path.join(self.work_dir, fn))
    @property
    def unpack_dir(self):
        return os.path.join(self.work_dir, self.unpack_name)

class ZipArchive(Archive):
    def __init__(self, url, work_dir, name):
        super(ZipArchive, self).__init__(url, work_dir, name)

    @property
    def unpack_name(self):
        with self.zipfile() as zf:
            return os.path.commonprefix(zf.namelist())

    def zipfile(self):
        return zipfile.ZipFile(self.path)

    def unpack(self):
        with self.zipfile() as zf: zf.extractall(self.work_dir)

class TarArchive(Archive):
    def __init__(self, url, work_dir, name, compression='gz'):
        super(TarArchive, self).__init__(url, work_dir, name)

        self.compression = compression

    @property
    def unpack_name(self):
        with self.tarfile() as tf:
            return os.path.commonprefix(tf.getnames())

    def tarfile(self):
        return tarfile.open(self.path, mode='r:%s' % self.compression)

    def unpack(self):
        with self.tarfile() as tf: tf.extractall(self.work_dir)

class MsiArchive(Archive):
    def __init__(self, url, work_dir, name, compression='gz'):
        super(MsiArchive, self).__init__(url, work_dir, name)

    @property
    def unpack_name(self):
        return '.'

    def unpack(self):
        self.system('msiexec /quiet /i %s' % self.path)

class GitArchive(Archive):
    def __init__(self, url, work_dir, name):
        super(GitArchive, self).__init__(url, work_dir, name)

        try:
            self.tag = self.url.split('#')[1]
        except IndexError:
            self.tag = None

    @property
    def unpack_name(self):
        return self.name + '-build'

    def unpack(self):
        subprocess.check_call(('git', 'clone', self.path, self.unpack_dir))

        if self.tag:
            subprocess.check_call(('git', '-C', self.unpack_dir, 'fetch', self.tag))
            subprocess.check_call(('git', '-C', self.unpack_dir, 'tag', self.tag, 'FETCH_HEAD'))
            subprocess.check_call(('git', '-C', self.unpack_dir, 'checkout', self.tag, '--quiet'))

    def download(self):
        winbrew.util.rm_rf(self.work_dir)
        winbrew.util.mkdir_p(self.work_dir)

        subprocess.check_call(('git', 'clone', self.url, self.path))

class ExeArchive(Archive):
    def __init__(self, url, work_dir, name):
        super(ExeArchive, self).__init__(url, work_dir, name)

    @property
    def unpack_name(self):
        return '.'

    def unpack(self):
        pass
