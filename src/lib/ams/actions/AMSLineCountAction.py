

from .AMSBaseAction import * 

class AMSLineCountAction(AMSBaseAction):
    """
    Counts non-empty lines in a file

    Parameters:
    path: path to the file
    """

    name = "filesystem.file.lineCount"

    def measure(self):
        path = self.getConfig().get("path", "/")
        s = 0 
        f = open(path, "r")
        for l in f:
            if l != "":
                s += 1
        return s
