
from ..lib.database import MakoDatabase 
from ..lib.schedule import * 
from ..lib.reporting import * 
from ..lib.ams import * 
from ..lib.table import * 

import os 
import os.path
import datetime
from datetime import date 
import shutil

from termcolor import colored 

from .MakoDesktopDatabase import *

from odspy import *

class MakoODSDesktopDatabase(MakoDesktopDatabase):

    """
    Params to constructor:

    path: path to the db 
    """
    
    def warn(self, text):
        print(colored("WARNING: ", "red") + " " + text)


    def uploadSchedules(self, schedules):
        raise NotImplementedError("This type of database setup does not support adding new schedules.")

    def downloadSchedules(self):
        res = [] 
        path = "%s/Schedule/Schedules by week/" % self.getParams()["path"] 
        ods_list = [ p for p in os.listdir(path) if p.endswith(".ods")]
        for name in ods_list:
            d = None
            try:
                d = datetime.datetime.strptime(name, "%Y.%m.%d.ods")
            except ValueError:
                self.warn("Schedule with filename %s does not contain correct format, skipping" % name) 
            doc = ODSDocument(path+name)
            times = {
                "01:00:00 AM": 1,
                "02:00:00 AM": 2,
                "03:00:00 AM": 3,
                "04:00:00 AM": 4,
                "05:00:00 AM": 5,
                "06:00:00 AM": 6,
                "07:00:00 AM": 7,
                "08:00:00 AM": 8,
                "09:00:00 AM": 9,
                "10:00:00 AM": 10,
                "11:00:00 AM": 11,
                "12:00:00 AM": 0,
                "01:00:00 PM": 13,
                "02:00:00 PM": 14,
                "03:00:00 PM": 15,
                "04:00:00 PM": 16,
                "05:00:00 PM": 17,
                "06:00:00 PM": 18,
                "07:00:00 PM": 19,
                "08:00:00 PM": 20,
                "09:00:00 PM": 21,
                "10:00:00 PM": 22,
                "11:00:00 PM": 23,
                "12:00:00 PM": 12,
            }
            s = Schedule(d)
            for row in doc.rows: 
                if not row[0].value in times.keys():
                    continue
                for i, cell in enumerate(row[1:]):
                    cell.value = cell.value.replace("–", "-")
                    cell.value = cell.value.replace("R&D", "Research and development")
                    if " - " in cell.value:
                        day = i+1
                        start = times[row[0].value]
                        duration = cell.number_rows_spanned
                        pname = cell.value.split(" - ")[0].lower()
                        spname = cell.value.split(" - ")[1].lower()
                        project = None
                        subproject = None
                        try:
                            project = [p for p in self.downloadProjects() if p.getName().lower() == pname.strip()][0]
                        except IndexError:
                            self.warn("Cannot get project by name: %s" % pname)
                            continue
                        try:
                            subproject = [p for p in project.getSubprojects() if p.getName().lower() == spname.strip()][0]
                        except IndexError:
                            self.warn("Cannot get subproject by name: %s" % spname)
                            continue
                        s.addEntry(ScheduleEntry(project, subproject, day, start, duration))
            res.append(s)
        return res
