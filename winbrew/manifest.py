import winbrew
import os
import pickle

class Manifest:
    """
    Stores a list of all files installed by a formula.  This class is used to 
    determine which files to uninstall, and to check for conflicts between
    formulas.
    """
    def __init__(self, name):
        self.files = []
        self.name = name
        self.path = os.path.abspath(os.path.join(winbrew.manifest_path, self.name))

    def save(self):
        """
        Write the manifest to the manifest file directory 
        """
        dirs = os.path.split(self.path)[0]
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        with open(self.path, 'wb') as fd:
            pickle.dump(self.files, fd, pickle.HIGHEST_PROTOCOL)
        
    def load(self):
        """ 
        Read the manifest from the manifest file directory
        """
        try:
            with open(self.path, 'rb') as fd:
                self.files = pickle.load(fd) 
        except IOError, e:
            self.files = []

    def delete(self):
        """
        Delete the manifest
        """
        os.remove(self.path)

    @property
    def installed(self):
        """
        Returns true if the Manifest indicates the formula is installed
        """
        try:
            open(self.path, 'rb').close()
            return True
        except IOError, e:
            return False

    @staticmethod
    def all():
        """ 
        List all installed packages
        """
        manifest = []
        for fn in os.listdir(winbrew.manifest_path):
            manifest.append(Manifest(fn))
        return manifest
            
            
        

