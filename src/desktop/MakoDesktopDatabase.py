
from ..lib.database import MakoDatabase 
from ..lib.schedule import * 
from ..lib.reporting import * 
from ..lib.ams import * 
from ..lib.schedule.formats import * 

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
        path = "%s/Measurements/" % self.path
        for name in os.listdir(path):
            fpath = "%s/%s/data.csv" % (path, name)
            apath =  "%s/%s/measure.json" % (path, name)
            ams = AMS()
            f = open(apath)
            action = ams.getAction(json.loads(f.read()))
            f.close()
            if action.getIdentifier() == action_id:
                f = open(fpath, "w")
                for line in data:
                    f.write(datetime.datetime.strftime(line[0], "%d.%m.%Y.") + "," + str(line[1]) + "\n")
                f.close()

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
        res = []
        path = "%s/Measurements/" % self.path
        for name in os.listdir(path):
            fpath = "%s/%s/measure.json" % (path, name)
            if os.path.isfile(fpath):
                ams = AMS()
                f = open(fpath)
                action = ams.getAction(json.loads(f.read()))
                f.close()
                res.append(action)
        return res



    def downloadMeasurementData(self, action_id):
        """
        data is list of tuples sorted by date from odler to newer

        first element in tuple is date 
        second element is value 
        """
        res = []
        path = "%s/Measurements/" % self.path
        for name in os.listdir(path):
            fpath = "%s/%s/data.csv" % (path, name)
            apath =  "%s/%s/measure.json" % (path, name)
            ams = AMS()
            f = open(apath)
            action = ams.getAction(json.loads(f.read()))
            f.close()
            if os.path.isfile(fpath) and action.getIdentifier() == action_id:
                f = open(fpath)
                header = True
                for line in f:
                    if header:
                        header = False 
                        continue
                    else:
                        date_str = line.split(",")[0]
                        val = float(line.split(",")[1])
                        d = datetime.datetime.strptime(date_str, "%d.%m.%Y.")
                        res.append((d, val))
        return res

    def downloadData(self):
        """
        Returns list of tuples where first element is name and second is data 
        """
        pass


    def downloadSchedules(self):
        res = [] 
        path = "%s/Schedules/" % self.path 
        sff_list = os.listdir(path)
        for name in sff_list:
            if os.path.isfile("%s/%s"% (path, name)) and name[-4:] == ".sff":
                reader = SFFReader()
                reader.open(filename="%s/%s" % (path, name))
                reader.read()
                reader.close()
                res.append((reader.getDate(), reader.readProjects(), reader.readEntries()))
        return res



    def downloadReports(self):
        res = []
        path = "%s/Reports/" % self.path 
        for name in os.listdir(path):
            if name[-5:] == ".json":
                f = open("%s/%s" % (path, name))
                json_data = f.read()
                r = Report("Blank", None)
                r.fromJSON(json_data)
                res.append(r)
                f.close()
        return res
