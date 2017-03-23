
from .. import ScheduleWriter


class SFFWriter(ScheduleWriter):
    """
    Parameters to constructor:

    filename: name of file to write in
    day: day of creation 
    month: month of creation
    year: year of creation
    """

    def write(self):
        params = self.getParams()
        entries = self.getEntries()
        projects = self.getProjects()
        fname = params.get("filename", "schedule.sff")
        self.file = open(fname, "wb")
        day, month, year = (params.get("day", 1), params.get("month", 1), params.get("year", 2017))
        self.file.write(bytes([day, month, (year >> 24) & 0xff, (year >> 16) & 0xff, (year >> 8) & 0xff, year & 0xff]))
        self.file.write(bytes([len(projects)]))
        for p in projects:
            bg, fg = (p.getBackgroundColor(), p.getForegroundColor())
            bgr, bgg, bgb = bg 
            fgr, fgg, fgb = fg 
            self.file.write(bytes([bgr, bgg, bgb, fgr, fgg, fgb]))
            self.file.write(bytes([len(p.getName())]))
            self.file.write(p.getName().encode("UTF-8"))
            self.file.write(bytes([len(p.getSubprojects())]))
            for sp in p.getSubprojects():
                self.file.write(bytes([len(sp.getName())]))
                self.file.write(sp.getName().encode("UTF-8"))
        self.file.write(bytes([len(entries)]))
        for e in entries:
            pid, sid = (0,0)
            for i in range(len(projects)):
                if projects[i].getName() == e.getProject().getName():
                    pid = i
                    for j in range(len(projects[i].getSubprojects())):
                        if e.getSubproject().getName() == projects[i].getSubprojects()[j].getName():
                            sid = j
            self.file.write(bytes([pid, sid, (e.getDay() << 5) + e.getStart(), e.getDuration()]))
    
    def close(self):
        self.file.close()
