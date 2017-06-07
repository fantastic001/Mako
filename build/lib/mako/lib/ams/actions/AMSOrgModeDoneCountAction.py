

from .AMSBaseAction import * 

from YAPyOrg import * 

class AMSOrgModeDoneCountAction(AMSBaseAction):
    """
    Counts DONE sections in a .org file

    Parameters:
    path: path to the file
    """


    name = "org.sections.done.count"

    def measure(self):
        s = 0
        f = ORGFile(self.getConfig().get("path", "sections.org"))
        doc = f.getDocument()
        elems = doc.getElements()
        for elem in elems:
            if elem.getType() == ORGElement.ELEMENT_TYPE_SECTION and elem.isDONE():
                s += 1
        return s
