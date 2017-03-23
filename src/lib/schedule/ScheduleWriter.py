
class ScheduleWriter(object):
    """
    How to use:

    writer = ScheduleWriter(entries, projects, param1=val1, param2=val2, ...)
    writer.write()
    writer.close()
    """

    def __init__(self, entries, projects = None, **params):
        self.entries = entries 
        if projects == None:
            self.projects = [] 
        else:
            self.projects = projects 
        for e in entries:
            fp = None
            for p in self.projects:
                if p.getName() == e.getProject().getName():
                    fp = p 
                    break 
            if fp == None:
                np = ScheduleProject(np.getName(), fp.getBackgroundColor(), fp.getForegroundColor())
                np.addSubproject(e.getSubproject())
            else:
                fp.addSubproject(e.getSubproject())
        self.params = params

    def getEntries(self):
        return self.entries 

    def getProjects(self):
        return self.projects

    def getParams(self):
        return self.params

    def write(self):
        """
        This method implements concrete writeing mechanism. 

        Entries, projects and parameters to the writer can be accessed via getEntries, getProjects and getParams methods respectively.
        """
        pass

    def close(self):
        """
        Implements closing writer stream.
        """
        pass
