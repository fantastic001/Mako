
from .. import ReportGenerator
from .. import Report

class QuarterReportGenerator(ReportGenerator):
    """
    This generator generates report based on quarter statistics. 

    You have to pass which quarter to be scored and what values. This can be done through setup(...) method like this:

        generator.setup(1, True, False)

    This will setup generator to generate quarter report reporting  for quarter 1 with time estimates but not with real times. 

    Report skeleton:

    field       type    description
    projects    list    List of projects for this quarter
    subprojects dict    for every project dictionary maps project's name to dictionary containing:

                        field       type    description 
                        subprojects list    list of subprojects
                        expected    dict    for each subproject dictionary maps subproject's name to sum of 
                                            time estimates for this quarter for this subproject.
                        real        dict    for each subproject dictionary maps subproject's name to sum of
                                            real time spent on tasks for this quarter.
    """
    
    def setup(self, year, quarter, expected, real):
        self.quarter = quarter
        self.expected = expected
        self.real = real
        self.year = year

    def inQuarter(self, task):
        return task.getDueDate().year == self.year and ((self.quarter == 1 and task.getDueDate().month in [1, 2, 3]) or (self.quarter == 2 and task.getDueDate().month in [4, 5, 6]) or (self.quarter == 3 and task.getDueDate().month in [7, 8, 9]) or (self.quarter == 4 and task.getDueDate().month in [10, 11, 12]))

    def generate(self):
        projects = self.getProjects()
        report = Report()
        report.setField("projects", [])
        report.setField("subprojects", {})
        for project in projects:
            report.getField("projects").append(project.getName())
            d = {}
            d["subprojects"] = []
            if self.expected:
                d["expected"] = {}
            if self.real:
                d["real"] = {}
            for subproject in project.getSubprojects():
                d["subprojects"].append(subproject.getName())
                if self.expected:
                    d["expected"][subproject.getName()] = 0
                    for task in subproject.getAllTasks():
                        if self.inQuarter(task):
                            d["expected"][subproject.getName()] += task.getExpectedTime()
                if self.real:
                    d["real"][subproject.getName()] = 0
                    for task in subproject.getAllTasks():
                        if self.inQuarter(task):
                            d["real"][subproject.getName()] += task.getSpentTime()
            report.getField("subprojects")[project.getName()] = d
        return report
