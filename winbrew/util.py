import errno
import os
import shutil
import stat

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: 
            raise 

def rm_rf(path):
    def onerror(func, path, exc_info):
       """
       Error handler for ``shutil.rmtree``.
   
       If the error is due to an access error (read only file)
       it attempts to add write permission and then retries.
   
       If the error is for another reason it re-raises the error.
   
       Usage : ``shutil.rmtree(path, onerror=onerror)``
       """
       if not os.access(path, os.W_OK):
           # Is the error an access error ?
           os.chmod(path, stat.S_IWUSR)
           func(path)
       else:
           raise
    if os.path.isdir(path):
        shutil.rmtree(path, onerror=onerror)
    elif os.path.isfile(path):
        os.remove(path)
    

