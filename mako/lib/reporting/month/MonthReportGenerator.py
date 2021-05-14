
from .. import Report 
from .. import ReportGenerator 

import datetime

class MonthReportGenerator(ReportGenerator):
    """
    This generator generates reports based on month statistics. 

    to setup generator, use setup(...)

    setup(...):
        month:          number of month to do statistics 
        time_per_task=3 maximal number of hours per task 
    
    Report structure:
        
        field           type        description

        expected_time   number      totl expected time for all tasks for a given month
        to_split        list        list of dictionaries where each element is tasks which has expected time > of maximal
            
            field       type        description

            project     string      project name
            subproject  string      subproject name 
            task        string      task text 
        
        expected_per_project: list  total time for each project, list of dictionaries:

            field       type        description
            
            project     string      project name
            time        int         number of hours
        
        impediments:    list        list of all tasks which took more time than expected in a given month, list of dictionaries:
            
            field       type        description

            project     string      project name
            subproject  string      subproject name
            task        string      task description
            expected    int         expected time
            spent       int         spent time
            
    """
    
    def in_month(self, task):
        return self.month == task.getDueDate().month and task.getDueDate().year == self.year

    def setup(self, year, month, time_per_task=2):
        self.month = month
        self.year = year
        self.time_per_task = time_per_task

    def generate(self):
        projects = self.getProjects()
        total = 0
        split = []
        report = Report("Monthly report for %d-%d" % (self.month, self.year), datetime.date.today())
        report.setField("to_split", [])
        report.setField("expected_per_project", [])
        report.setField("impediments", [])
        time = {}
        for project in self.getProjects():
            time[project.getName()] = 0
            for subproject in project.getSubprojects():
                for task in subproject.getAllTasks():
                    if self.in_month(task):
                        time[project.getName()] += task.getExpectedTime()
                        total += task.getExpectedTime()
                        if task.getExpectedTime() < task.getSpentTime():
                            report.getField("impediments").append({
                                "project": project.getName(),
                                "subproject": subproject.getName(),
                                "task": task.getText(),
                                "expected": task.getExpectedTime(),
                                "spent": task.getSpentTime()
                            })
                        if task.getExpectedTime() > self.time_per_task:
                            report.getField("to_split").append({
                                "project": project.getName(),
                                "subproject": subproject.getName(),
                                "task": task.getText()
                            })
        for p in time.keys():
            report.getField("expected_per_project").append({
                "project": p,
                "time": time[p]
            })
            
        report.setField("expected_time", total)
        return report
