
from .ScheduleProject import * 
from .ScheduleEntry import * 

class ScheduleWriter(object):
    """
    How to use:

    writer = ScheduleWriter(entries, projects, param1=val1, param2=val2, ...)
    writer.write()
    writer.close()
    """

    def __init__(self, schedule, **params):
        self.entries = schedule.getEntries()
        self.projects = []
        for e in self.entries:
            fp = None
            for p in self.projects:
                if p.getName() == e.getProject().getName():
                    fp = p 
                    break 
            if fp == None:
                fp = e.getProject()
                np = ScheduleProject(fp.getName(), fp.getBackgroundColor(), fp.getForegroundColor())
                np.addSubproject(e.getSubproject())
                self.projects.append(np)
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
