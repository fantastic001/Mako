
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
        report = Report("Monthly report for %s" % str(datetime.date.today()), datetime.date.today())
        report.setField("to_split", [])
        for project in self.getProjects():
            for subproject in project.getSubprojects():
                for task in subproject.getAllTasks():
                    if self.in_month(task):
                        total += task.getExpectedTime()
                        if task.getExpectedTime() > self.time_per_task:
                            report.getField("to_split").append({
                                "project": project.getName(),
                                "subproject": subproject.getName(),
                                "task": task.getText()
                            })
        report.setField("expected_time", total)
        return report
