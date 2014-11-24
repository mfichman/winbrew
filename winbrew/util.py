import errno
import os
import shutil

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: 
            raise 

def rm_rf(path):
    shutil.rmtree(path, ignore_errors=True)

