
import unittest 

import datetime

from ..lib.reporting.quarter import QuarterReportGenerator 
from ..lib.schedule import ScheduleProject, ScheduleSubproject, Task 

class TestQuarterReportGenerator(unittest.TestCase):
    
    def test_single_project(self):
        p = ScheduleProject("University", (0,0,0), (0,0,0))
        sp = ScheduleSubproject("Calculus")
        sp.addTask(Task("Task 1", 2, 0, False, datetime.date(2017, 1, 1)))
        sp.addTask(Task("Task 2", 2, 0, True, datetime.date(2017, 1, 5)))
        sp.addTask(Task("Task 3", 2, 0, True, datetime.date(2016, 1, 5)))
        p.addSubproject(sp)

        generator = QuarterReportGenerator([p])
        generator.setup(2017, 1, True, True)
        report = generator.generate()
        self.assertEqual(report.getField("projects"), ["University"])
        self.assertEqual(report.getField("subprojects")["University"]["expected"]["Calculus"], 4)
