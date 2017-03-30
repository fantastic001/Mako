

from .AMSBaseAction import * 

class AMSOrgModeDoneCountAction(AMSBaseAction):
    """
    Counts DONE sections in a .org file

    Parameters:
    path: path to the file
    """


    name = "org.sections.done.count"

    def measure(self):
        raise NotImplementedError
