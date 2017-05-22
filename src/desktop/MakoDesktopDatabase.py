
from ..lib.database import MakoDatabase 
from ..lib.schedule import * 
from ..lib.reporting import * 
from ..lib.ams import * 

import os 
import os.path
from datetime import date 

from YAPyOrg import * 

class MakoDesktopDatabase(MakoDatabase):

    def __init__(self, path):
        """
        path: path to the directory where database files are held 
        """
        self.path = path

    def uploadProjects(self, projects):
        pass

    def uploadMeasurementActions(self, actions):
        pass

    def uploadMeasurementData(self, action_id, data):
        """
        data is list of tuples sorted by date from odler to newer

        first element in tuple is date 
        second element is value 
        """
        pass

    def uploadData(self, data):
        """
        Data is list of tuples where first element is name and second concrete data 
        """
        pass

    def uploadSchedules(self, schedules):
        pass

    def uploadReports(self, reports):
        pass


    def readForeground(self, path):
        return (255, 255, 255)

    def readBackground(self, path):
        return (255, 0, 0)

    def parseDate(self, element):
        title = element.getTitle() 
        month = 1
        year = 2000
        months = {
            "january": 1,
            "february": 2,
            "march": 3,
            "april": 4,
            "may": 5,
            "june": 6,
            "july": 7,
            "august": 8,
            "september": 9,
            "october": 10,
            "november": 11,
            "december": 12
        }
        elems = title.split(" ")
        if len(elems) >= 2:
            year = int(elems[1])
            month = months.get(elems[0], 1)
        return date(year, month, 28)


    def parseTask(self, element, last):
        title = element.getTitle()
        elems = title.split(" - ")
        desc = elems[0]
        expected = 0
        spent = 0
        if len(elems) > 1:
            if len(elems) >= 3:
                expected = int(elems[-2][:-1])
                spent = int(elems[-1][:-1])
            else:
                expected = int(elems[-1][:-1])
        return Task(desc, expected, spent, element.isDONE(), last)

    def readSubprojects(self, path):
        res = []
        for name in os.listdir(path):
            subproject = None
            spath = path + "/" + name + "/" 
            for fn in ["notes.org", "plan.org"]:
                if os.path.isfile("%s/%s" % (spath, fn)):
                    spath = "%s/%s" % (spath, fn)
                    subproject = ScheduleSubproject(name)
            if subproject != None:
                doc = ORGFile(spath).getDocument()
                elements = doc.getElements()
                start = 0
                for i in range(len(elements)):
                    if elements[i].getType() == ORGElement.ELEMENT_TYPE_SECTION:
                        if elements[i].getLevel() == 1 and elements[i].getTitle().lower() in ["time boxed", "time-boxed"]:
                            start = i 
                            break
                if start > 0:
                    last = datetime.date(2000, 1, 28)
                    for i in range(start+1, len(elements)):
                        if elements[i].getType() == ORGElement.ELEMENT_TYPE_SECTION:
                            if elements[i].getLevel() == 2:
                                last = self.parseDate(elements[i])
                            if elements[i].getLevel() == 3:
                                subproject.addTask(self.parseTask(elements[i], last))
                    res.append(subproject)
        return res 



    def downloadProjects(self):
        res = []
        for name in os.listdir(self.path + "/Projects/"):
            path = "%s/Projects/%s/" % (self.path, name)
            if os.path.isdir(path):
                project = ScheduleProject(name, self.readBackground(path), self.readForeground(path))
                subprojects = self.readSubprojects(path)
                for sp in subprojects:
                    project.addSubproject(sp)
                res.append(project)
        return res

    def downloadMeasurementActions(self):
        pass

    def downloadMeasurementData(self, action_id):
        """
        data is list of tuples sorted by date from odler to newer

        first element in tuple is date 
        second element is value 
        """
        pass

    def downloadData(self):
        """
        Returns list of tuples where first element is name and second is data 
        """
