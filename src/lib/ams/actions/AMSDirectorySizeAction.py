
from .AMSBaseAction import * 

import os 

class AMSDirectorySizeAction(AMSBaseAction):
    """
    Measures size of specified directory in MB

    Parameters:
    path: path to the directory which size is being measured
    """


    name = "filesystem.directory.size"

    def getDirectorySize(self, path):
        total = 0
        for entry in os.scandir(path):
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += self.getDirectorySize(entry.path)
        return total

    def measure(self):
        path = self.getConfig().get("path", "/")
        return self.getDirectorySize(path) / 2**20
