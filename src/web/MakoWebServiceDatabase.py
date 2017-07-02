
from ..lib.database import MakoDatabase 
from ..lib.schedule import * 
from ..lib.reporting import * 
from ..lib.ams import * 
from ..lib.schedule.formats import * 
from ..lib.table import * 


class MakoWebServiceDatabase(MakoDatabase):

    def __init__(self, webservice):
        """
        webservice: object of class which implements MakoWebService
        """
        self.webservice = webservice

    def uploadList(self, identifier, items):
        d = {}
        d[identifier] = [] 
        for item in items:
            d[identifier].append(item.toDict())
        self.webservice.uploadData(identifier, json.dumps(d,  indent=4))

    def downloadList(self, identifier, typeOfObject):
        data = self.webservice.downloadData(identifier)
        d = json.loads(data)
        items = d[identifier]
        res = [] 
        for item in items:
            res.append(typeOfObject.fromDict(item))
        return res

    def uploadProjects(self, projects):
            self.uploadList("projects", projects)

    def uploadMeasurementActions(self, actions):
        self.uploadList("metrics", actions)

    def uploadMeasurementData(self, action_id, data):
        """
        data is list of tuples sorted by date from odler to newer

        first element in tuple is date 
        second element is value 
        """
        sss = ""
        for line in data:
            sss += datetime.datetime.strftime(line[0], "%d.%m.%Y.") + "," + str(line[1]) + "\n"
        self.webservice.uploadData("%s-DATA" % action_id, sss)

    def uploadData(self, data):
        """
        Data is list of tuples where first element is name and second concrete data 
        """
        pass

    def uploadSchedules(self, schedules):
        self.uploadList("schedules", schedules)

    def uploadReports(self, reports):
        self.uploadList("reports", reports)

    def uploadDefaultConditions(self, conditions):
        self.uploadList("conditions", conditions)

    def uploadTables(self, tables):
        self.uploadList("tables", tables)

    def downloadProjects(self):
        return self.downloadList("projects", ScheduleProject)

    def downloadMeasurementActions(self):
        data = self.webservice.downloadData("metrics")
        ams = AMS()
        res = []
        d = jon.loads(data)
        for a in d["metrics"]:
            action = ams.getAction(json.loads(a))
            res.append(action)
        return res
    def downloadMeasurementData(self, action_id):
        """
        data is list of tuples sorted by date from odler to newer

        first element in tuple is date 
        second element is value 
        """
        data = self.webservice.downloadData("%s-DATA" % action_id)
        res = [] 
        for line in data.split("\n"):
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
        return self.downloadList("schedules", Schedule)

    def downloadReports(self):
        return self.downloadList("reports", Report)

    def downloadDefaultConditions(self):
        return self.downloadList("conditions", ScheduleCondition)

    def downloadTables(self):
        return self.downloadList("tables", Table)
