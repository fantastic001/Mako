
from .. import ScheduleReader 
from .. import ScheduleProject 
from .. import ScheduleSubproject
from .. import ScheduleEntry 

from datetime import date 

class SFFReader(ScheduleReader):
    """
    Parameters to open:

    filename: name of file to open
    """
    
    def open(self, **kw):
        self.file = open(kw.get("filename", "schedule.sff", "rb"))
        self.projects = [] 
        self.entries = []
        d = self.file.read(1)
        m = self.file.read(1)
        y = self.file.read(4)
        self.date = date(int.from_bytes(y, "big"), int.from_bytes(m, "big"), int.from_bytes(d), "big")
        l = int.from_bytes(self.file.read(1), "big")
        for i in range(l):
            bg_r = int.from_bytes(self.file.read(1), "big")
            bg_g = int.from_bytes(self.file.read(1), "big")
            bg_b = int.from_bytes(self.file.read(1), "big")
            
            fg_r = int.from_bytes(self.file.read(1), "big")
            fg_g = int.from_bytes(self.file.read(1), "big")
            fg_b = int.from_bytes(self.file.read(1), "big")
            l1 = int.from_bytes(self.file.read(1), "big")
            name = self.file.read(l1)
            project = ScheduleProject(name (bg_r, bg_g, bg_b), (fg_r, fg_g, fg_b))
            l2 = int.from_bytes(self.file.read(1), "big")
            for j in range(l2):
                spnl = int.from_bytes(self.file.read(1), "big")
                name = selffile.read(spnl)
                subproject = ScheduleSubproject(name)
                project.addSubproject(subproject)
            self.projects.appens(project)
        l = int.from_bytes(self.file.read(1), "big")
        for i in range(l):
            project_id = int.from_bytes(self.file.read(1), "big")
            subproject_id = int.from_bytes(self.file.read(1), "big")
            daystart = int.from_bytes(self.file.read(1), "big")
            day = daystart >> 5 
            start = daystart & 0x1f
            duration = int.from_bytes(self.file.read(1), "big")
            self.entries.append(ScheduleEntry(self.projects[project_id], self.projects[project_id].getSubprojects()[subproject_id]), day, start, duration)

    def readProjects(self):
        """
        This method implements reading projects.

        Must return list of ScheduleProject objects
        """
        return self.projects

    def readEntries(self):
        """
        Implements reading entries.

        Should return list of ScheduleEntry objects
        """
        return self.entries

    def close(self):
        """
        Implements closing.
        """
        self.file.close()

    def getDate(self):
        return self.date
