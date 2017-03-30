


from .AMSBaseAction import * 

class AMSOrgModeSectionCountAction(AMSBaseAction):
    """
    Counts sections in a .org file

    Parameters:
    path: path to the file
    """


    name = "org.sections.count"

    def measure(self):
        raise NotImplementedError
