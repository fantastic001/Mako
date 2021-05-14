
from ..schedule import * 
from ..reporting import * 
from ..ams.actions import * 
from ..ams import * 

from typing import *

class MakoDatabase(object):
    """
    Abstract class which all supported databases have to implement
    """
    def __init__(self, **params):
        """
        Initialize database 

        keyword arguments depend on specific database used
        """
        self.params = params
        if not self.validate():
            self.init()

    def getParams(self):
        """
        Returns dictionary of parameters supplied to constructor. This function has to be called only within concrete database implementation class. 
        
        Returns: dictionary where keys are parameter names and values are values supplied as keyword parameters to constructor. 
        """
        return self.params

    def init(self):
        """
        Implementation of database has to implement. 

        Initialize database (assume it does not exist).
        """
        pass

    def validate(self):
        """
        Implementation of database has to implement. 

        Verify if database is created. Returns True if it exists or False if it does not.
        """
        pass

    def uploadProjects(self, projects):
        """
        Implementation of database has to implement. 

        Perform writing of list of projects to database. 

        Args:
            projects: list of ScheduleProject objects.
        """
        pass

    def uploadMeasurementActions(self, actions):
        """
        Implementation of database has to implement. 

        Writes measurement actions to database. 

        Args:
            actioins: list of BaseAction or derived objects.
        """
        pass

    def uploadMeasurementData(self, action_id, data):
        """
        Implementation of database has to implement. 

        data is list of tuples sorted by date from odler to newer

        first element in tuple is date 
        second element is value 

        Args:
            action_id: action id for which data is uploaded (see name field for every action implementation)
            data: data structured as explained above
        """
        pass

    def uploadData(self, data):
        """
        Implementation of database has to implement.

        Data is list of tuples where first element is name and second concrete data 

        Args:
            data: data structured as explained above
        """
        pass

    def uploadSchedules(self, schedules):
        """
        Implementation of database has to implement.

        Args:
            schedules: list of Schedule objects:

        """
        pass

    def uploadReports(self, reports):
        """
        Implementation of database has to implement.

        Args:
            reports: list of Report objects

        """
        pass

    def uploadDefaultConditions(self, conditions):
        """
        Implementation of database has to implement.

        default conditions are schedule coonditions applied for every schedule by default and they are added by user. 

        Args:
            conditions: list of ScheduleCondition objects

        """
        pass

    def uploadTables(self, tables):
        """
        Implementation of database has to implement.

        Args:
            tables: list of Table objects

        """
        pass

    def downloadProjects(self):
        """
        Implementation of database has to implement.

        Returns: list of ScheduleProject objects

        """
        pass

    def downloadMeasurementActions(self):
        """
        Implementation of database has to implement.

        Returns: list of BaseAction objects
        """
        pass

    def downloadMeasurementData(self, action_id):
        """
        Implementation of database has to implement.
        data is list of tuples sorted by date from odler to newer

        first element in tuple is date 
        second element is value 
        Args:
            action_id: action name for which data is requested.
        Returns: data

        """
        pass

    def downloadData(self):
        """
        Implementation of database has to implement.

        Returns: list of tuples where first element is name and second is data 
        """
        pass

    def downloadSchedules(self):
        """
        Implementation of database has to implement.

        Returns: list of Schedule object
        """
        pass

    def downloadReports(self):
        """
        Implementation of database has to implement.

        Returns: list of Report objects
        """
        pass

    def downloadDefaultConditions(self):
        """
        Implementation of database has to implement.

        Returns: list of ScheduleCondition objects
        """
        pass

    def downloadTables(self):
        """
        Implementation of database has to implement.

        Returns: list of Table objects
        """
        pass

    def toDict(self):
        """
        Get contents of database as dictionary

        Returns: dictionary
        """
        d = {}
        d["projects"] = [] 
        projects = self.downloadProjects()
        for project in projects:
            d["projects"].append(project.toDict())
        
        d["schedules"] = []
        schedules = self.downloadSchedules()
        for schedule in schedules:
            d["schedules"].append(schedule.toDict())

        d["default_conditions"] = []
        for condition in self.downloadDefaultConditions():
            d["default_conditions"].append(condition.toDict())

        metrics = self.downloadMeasurementActions()
        d["metrics"] = [] 
        d["data"] = []
        for metric in metrics:
            d["metrics"].append(metric.toDict())
            data = self.downloadMeasurementData(metric.getIdentifier())
            dd = {"id": metric.getIdentifier()}
            dd["data"] = [] 
            for val in data:
                dd["data"].append({"date": datetime.datetime.strftime(val[0], "%Y-%m-%d"), "value": val[1]})
            d["data"].append(dd)
        d["reports"] = [] 
        reports = self.downloadReports()
        for report in reports:
            d["reports"].append(report.toDict())

        d["tables"] = []
        tables = self.downloadTables()
        for table in tables:
            d["tables"].append(table.toDict())
        return d

    def fromDict(self, d):
        """
        For given dictionary (same format as toDict returns), load supplied data to database and overwrite existing data in database. 

        Args:
            d: dictionary containing data in samme format as one toDict returns
        """
        projects = []
        for project in d["projects"]:
            projects.append(ScheduleProject.fromDict(project))
        self.uploadProjects(projects)
        
        schedules = []
        for schedule in d["schedules"]:
            schedules.append(Schedule.fromDict(schedule))
        self.uploadSchedules(schedules)
        
        conditions = [] 
        for condition in d["default_conditions"]:
            conditions.append(ScheduleCondition.fromDict(condition))
        self.uploadDefaultConditions(conditions)
        
        ams = AMS()
        metrics = []
        for metric in d["metrics"]:
            metrics.append(ams.getAction(metric))
        self.uploadMeasurementActions(metrics)

        reports = []
        for report in d["reports"]:
            reports.append(Report.fromDict(report))
        self.uploadReports(reports)

        for data_obj in d["data"]:
            data = []
            for val in data_obj["data"]:
                data.append((datetime.datetime.strptime(val["date"], "%Y-%m-%d"), float(val["value"])))
            self.uploadMeasurementData(data_obj["id"], data)
        
        tables = [] 
        for table in d["tables"]:
            tables.append(Table.fromDict(table))
        self.uploadTables(tables)

    def export(self, db):
        """
        Exports data from current datatbase to database in argument 'db'

        This method also does validation and initialization of ndatabase 'db' if needed

        Args:
            db: MakoDatabase object to export to.
        """
        db.uploadProjects(self.downloadProjects())
        actions = self.downloadMeasurementActions()
        db.uploadMeasurementActions(actions)
        for action in actions:
            db.uploadMeasurementData(action.getIdentifier(), self.downloadMeasurementData(action.getIdentifier()))
        db.uploadData(self.downloadData())
        db.uploadSchedules(self.downloadSchedules())
        db.uploadTables(self.downloadTables())
        db.uploadReports(self.downloadReports())
        db.uploadDefaultConditions(self.downloadDefaultConditions())

    def diff(self, old):
        """
        Get difference in two databases. 

        Args:
            old: MakoDatabase object which difference is calculated relative to
        Returns:dict object with keys {"projects", "subprojects", "tasks", "schedules", "conditions", "reports", "tables", "data", "metrics", "measurements"}. 
        Every key has dict assigned with itself with two keys: "added" and "removed" which are liists of dict objects representing concrete items representation like toDict does. 
        """
        projects = self.downloadProjects()
        projects_ = old.downloadProjects()

        metrics = self.downloadMeasurementActions()
        metrics_ = old.downloadMeasurementActions()

        schedules = self.downloadSchedules()
        schedules_ = old.downloadSchedules()

        tables = self.downloadTables()
        tables_ = old.downloadTables()

        conditions = self.downloadDefaultConditions()
        conditions_ = old.downloadDefaultConditions()

        data = self.downloadData()
        data_ = old.downloadData()
        if data is None: data = []
        if data_ is None: data_ = []

        reports = self.downloadReports()
        reports_ = old.downloadReports()

        res = {
            "projects": {
                "added": set(p.getName() for p in projects) - set(p.getName() for p in projects_), 
                "removed": set(p.getName() for p in projects_) - set(p.getName() for p in projects)
            },
            "subprojects": {
                "added": set((p.getName(),s.getName()) for p in projects for s in p.getSubprojects()) - set((p.getName(),s.getName()) for p in projects_ for s in p.getSubprojects()),
                "removed": set((p.getName(),s.getName()) for p in projects_ for s in p.getSubprojects()) - set((p.getName(),s.getName()) for p in projects for s in p.getSubprojects())
            },
            "tasks": {
                "added": set((p.getName(),s.getName(), t) for p in projects for s in p.getSubprojects() for t in s.getAllTasks()) - set((p.getName(),s.getName(), t) for p in projects_ for s in p.getSubprojects() for t in s.getAllTasks()),
                "removed": set((p.getName(),s.getName(), t) for p in projects_ for s in p.getSubprojects() for t in s.getAllTasks()) - set((p.getName(),s.getName(), t) for p in projects for s in p.getSubprojects() for t in s.getAllTasks())
            },
            "schedules": {
                "added": set(schedules) - set(schedules_),
                "removed": set(schedules_) - set(schedules)
            },
            "tables": {
                "added": set(tables) - set(tables_),
                "removed": set(tables_) - set(tables)
            },
            "reports": {
                "added": set(reports) - set(reports_),
                "removed": set(reports_) - set(reports)
            },
            "metrics": {
                "added": set(metrics) - set(metrics_),
                "removed": set(metrics_) - set(metrics)
            },
            "conditions": {
                "added": set(conditions) - set(metrics_),
                "removed": set(conditions_) - set(metrics)
            },
            "data": {
                "added": set(data) - set(data_),
                "removed": set(data_) - set(data)
            },
            "measurements": {
                "added": set((a,m) for a in metrics for m in self.downloadMeasurementData(a.getIdentifier())) - set((a,m) for a in metrics_ for m in old.downloadMeasurementData(a.getIdentifier())),
                
                "removed": set((a,m) for a in metrics_ for m in old.downloadMeasurementData(a.getIdentifier())) - set((a,m) for a in metrics for m in self.downloadMeasurementData(a.getIdentifier())),
            }
        }
        for k,v in res.items():
            res[k]["added"] = list(res[k]["added"])
            res[k]["removed"] = list(res[k]["removed"])
        return res
