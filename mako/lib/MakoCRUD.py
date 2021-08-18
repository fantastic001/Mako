
from mako.loggers.BaseLogger import BaseLogger
from mako.loggers.Loggable import Loggable
from .schedule import * 
from .reporting import * 
from .ams import * 
from .table import *



class MakoCRUD(object):
    
    def __init__(self, db, logger: BaseLogger = None):
        if logger is not None:
            self.db = Loggable(db, logger)
        else: 
            self.db = db 
        self.listeners = []
    
    def addStatusListener(self, listener):
        self.listeners.append(listener)
    
    def publish(self, notification, *args):
        for listener in self.listeners:
            getattr(listener, "on" + notification)(*args)

    def visitProjects(self, callback):
        """
        For every project in database call callback(project)
        """
        projects = self.db.downloadProjects()
        for project in projects:
            callback(project)

    def addProject(self, p_name):
        projects = self.db.downloadProjects()
        if len(list([p.getName() for p in projects if p.getName() == p_name])) > 0:
            self.publish("Error", "Project with given name already exists")
            return 
        projects.append(ScheduleProject(p_name, (0,0,0), (0,0,0)))
        self.db.uploadProjects(projects)

    def deleteProject(self, project_name):
        projects = self.db.downloadProjects()
        newprojects = [] 
        for p in projects:
            if p.getName() != name:
                newprojects.append(p)
        self.db.uploadProjects(newprojects)

    def visitSubprojects(self, project_name, callback):
        """
        for every subproject in project given by project name, call callback(subproject)
        """
        def visitor(p):
            if p.getName() == project_name:
                for sp in p.getSubprojects():
                    if sp.isActive():
                        callback(sp)
        self.visitProjects(visitor)
    
    def visitLegacySubprojects(self, project_name, callback):
        """
        for every legacy subproject in project given by project name, call callback(subproject)
        """
        def visitor(p):
            if p.getName() == project_name:
                for sp in p.getSubprojects():
                    if not sp.isActive():
                        callback(sp)
        self.visitProjects(visitor)

    def addSubproject(self, project_name, subproject_name):
        projects = self.db.downloadProjects()
        for p in projects:
            if p.getName() == project_name:
                p.addSubproject(ScheduleSubproject(subproject_name))
                self.db.uploadProjects(projects)
                return 
        print("Project with given name not found")
        
    def deleteSubproject(self, project_name, subproject_name):
        projects = self.db.downloadProjects()
        for project in projects:
            if project.getName() == project_name:
                subprojects = project.getSubprojects()
                for sp in subprojects:
                    if sp.getName() != subproject_name:
                        sp.setActive(False)
        self.db.uploadProjects(projects)

    def visitTasks(self, project_name, subproject_name, callback):
        """
        For every task in given project's subproject, call callback(task, index) where index is index in task list
        """
        def visitor(sp):
            if sp.getName() == subproject_name:
                for i in range(len(sp.getAllTasks())): 
                    callback(sp.getAllTasks()[i], i)
        self.visitSubprojects(
            project_name,
            visitor
        )

    def addTask(self, pname, spname, text, due, expected):
        projects = self.db.downloadProjects()
        for p in projects:
            if p.getName() == pname:
                for sp in p.getSubprojects():
                    if sp.getName() == spname:
                        sp.addTask(Task(text, expected, due=due))
                        self.db.uploadProjects(projects)
                        return 
        print("Project or subproject with given name not found")

    def deleteTask(self, pname, spname, index):
        projects = self.db.downloadProjects()
        for p in projects:
            if p.getName() == pname:
                for sp in p.getSubprojects():
                    if sp.getName() == spname:
                        try:
                            tasks = sp.getAllTasks().copy()
                            del tasks[index]
                        except IndexError:
                            print("Wrong index of the task")
                        else:
                            sp.deleteAllTasks()
                            for t in tasks:
                                sp.addTask(t)
                            self.db.uploadProjects(projects)
                        return 

    def markTaskDone(self, pname, spname, i):
        projects = self.db.downloadProjects()
        for p in projects:
            if p.getName() == pname:
                for sp in p.getSubprojects():
                    if sp.getName() == spname:
                        try:
                            sp.getAllTasks()[i].setDone()
                        except IndexError:
                            print("Wrong task index")
        self.db.uploadProjects(projects)

    def increaseSpentTime(self, pname, spname, index, dt):
        dt = int(dt)
        projects = self.db.downloadProjects()
        for p in projects:
            if p.getName() == pname:
                for sp in p.getSubprojects():
                    if sp.getName() == spname:
                        try:
                            sp.getAllTasks()[index].increaseSpentTime(dt)
                        except IndexError:
                            print("Wrong task index")
        self.db.uploadProjects(projects)

    def visitSchedules(self, callback):
        schedules = self.db.downloadSchedules()
        for schedule in schedules:
            callback(schedule)

    def addSchedule(self):
        schedules = self.db.downloadSchedules()
        s = Schedule(datetime.date.today())
        for condition in self.db.downloadDefaultConditions():
            s.addCondition(condition)
        schedules.append(s)
        self.db.uploadSchedules(schedules)

    def performOnLastSchedule(self, callback, error_callback):
        """
        Performs operation on last schedule calling callback(schedule) and saves everything to database 

        If errors are found (condition not satisfied in schedule), then for each error error_callback(error) is called and 
        data is not saved to db. You can acces description of condition with error.getDescription().
        """
        schedules = sorted(self.db.downloadSchedules(), key=lambda x: x.getDate())
        try:
            callback(schedules[-1])
            errors = schedules[-1].check()
        except IndexError as e:
            raise e
            print("There is no schedule created yet")
        else:
            for error in errors:
                error_callback(error[1].getDescription())
            if len(errors) == 0: self.db.uploadSchedules(schedules)
    
    def visitTasksToday(self, callback):
        """
        callback(project, subproject, task)
        """
        self.performOnLastSchedule(lambda x: [callback(p,sp,t) for p,sp,t in x.tasksToday(self.db.downloadProjects(), datetime.date.today().weekday()+1)], lambda text: None)

    def addEntryToLastSchedule(self, day, time, duration, project_name, subproject_name, error_callback):
        projects = self.db.downloadProjects()
        try:
            project = list(filter(lambda p: p.getName() == project_name, projects))[0]
            subproject = list(filter(lambda sp: sp.getName() == subproject_name, project.getSubprojects()))[0]
        except IndexError:
            print("Given project or subproject not found")
        else:
            self.performOnLastSchedule(lambda s: s.addEntry(ScheduleEntry(project, subproject, day, time, duration)), error_callback)

    def removeEntry(self, day, start, duration):
        self.performOnLastSchedule(lambda s: s.removeEntry(int(day), int(start), int(duration)), lambda e: print("ERROR:" + e.getDescription()))

    def measureAll(self, callback):
        """
        Measures all metrics and saves them to db. For every measured metric is called callback(metric, value)
        """
        actions = self.db.downloadMeasurementActions()
        ams = AMS()
        tables = self.db.downloadTables()
        for action in actions:
            metric = action
            data = self.db.downloadMeasurementData(metric.getIdentifier())
            val = metric.measure(tables)
            callback(metric, val)
            data.append((datetime.date.today(), val))
            self.db.uploadMeasurementData(metric.getIdentifier(), data)

    def visitMetrics(self, callback):
        """
        For every metric call callback(metric, data)
        """
        actions = self.db.downloadMeasurementActions()
        ams = AMS()
        for action in actions:
            data = db.downloadMeasurementData(action.getIdentifier())
            callback(action, data)

    def visitReports(self, callback):
        """
        For every report call callback(report)
        """
        reports = self.db.downloadReports()
        for report in reports:
            callback(report)

    def generateMonthlyReport(self, year, month):
        generator = MonthReportGenerator(self.db.downloadProjects())
        generator.setup(int(year), int(month))
        report = generator.generate()
        reports = self.db.downloadReports()
        reports.append(report)
        self.db.uploadReports(reports)

    def generateQuarterlyReport(self, year, quarter):
        generator = QuarterReportGenerator(self.db.downloadProjects())
        generator.setup(int(year), int(quarter), True, True)
        report = generator.generate()
        reports = self.db.downloadReports()
        reports.append(report)
        self.db.uploadReports(reports)

    def showReport(self, report_name, views):
        reports = self.db.downloadReports()
        r = None
        for report in reports:
            if report.getName() == report_name:
                r = report 
                break
        for view in views:
            view.show(r)

    def visitTables(self, callback):
        tables = self.db.downloadTables()
        for table in tables:
            callback(table)
    
    def performOnTables(self, callback):
        tables = self.db.downloadTables()
        for table in tables:
            callback(table)
        self.db.uploadTables(tables)
        

    def addTable(self, table_name, fields):
        t = Table(table_name, fields.split("|"))
        tables = self.db.downloadTables()
        tables.append(t)
        self.db.uploadTables(tables)

    def deleteTable(self, tname):
        res = [] 
        def visitor(x):
            if x.getName() != tname:
                res.append(x)
        self.visitTables(visitor)
        self.db.uploadTables(x)

    def addTableEntry(self, tname, data):
        def visitor(table):
            if table.getName() == tname:
                table.addEntry(data.split("|"))
        self.performOnTables(visitor)

    def visitTableEntries(self, tname, callback):
        """
        call callback(entry, index) for each entry
        """
        def visitor(table):
            if table.getName() == tname:
                for i in range(len(table.getEntries())):
                    callback(table.getEntries()[i], i)
        self.visitTables(visitor)

    def deleteTableEntry(self, tname, eindex):
        def f(x):
            if x.getName() == tname:
                x.removeEntry(eindex)
        self.performOnTables(f)

    def updateTableEntry(self, tname, eindex, data):
        def f(x):
            if x.getName() == tname:
                x.updateEntry(int(eindex), data.split("|"))
        self.performOnTables(f)
