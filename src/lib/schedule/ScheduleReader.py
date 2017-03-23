

class ScheduleReader(object):
    """
    How to use:

    reader = ScheduleReader()
    reader.open(param1=val1, param2=val2, ...)
    reader.read()
    reader.close()

    projects = reader.getProjects()
    entries = reader.getEntries()
    """
    
    def open(self, **kw):
        """
        This method should implement opening file or stream.

        kw: parameters to the reader
        """
        pass

    def readProjects(self):
        """
        This method implements reading projects.

        Must return list of ScheduleProject objects
        """
        pass

    def readEntries(self):
        """
        Implements reading entries.

        Should return list of ScheduleEntry objects
        """
        pass

    def close(self):
        """
        Implements closing.
        """
        pass

    def read(self):
        self.entries = self.readEntries()
        self.projects = self.readProjects()
        
    def getEntries(self):
        return self.entries

    def getProjects(self):
        return self.projects
