


from .AMSBaseAction import * 

from YAPyOrg import * 

class AMSOrgModeSectionCountAction(AMSBaseAction):
    """
    Counts sections in a .org file

    Parameters:
    path: path to the file
    """


    name = "org.sections.count"

    def measure(self, tables):
        s = 0
        f = ORGFile(self.getConfig().get("path", "sections.org"))
        doc = f.getDocument()
        elems = doc.getElements()
        for elem in elems:
            if elem.getType() == ORGElement.ELEMENT_TYPE_SECTION:
                s += 1
        return s
