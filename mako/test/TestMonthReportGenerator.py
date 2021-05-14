
import unittest 

import datetime

from ..lib.reporting.month import MonthReportGenerator 
from ..lib.schedule import ScheduleProject, ScheduleSubproject, Task 

class TestMonthReportGenerator(unittest.TestCase):
    
    def test_single_project(self):
        p = ScheduleProject("University", (0,0,0), (0,0,0))
        sp = ScheduleSubproject("Calculus")
        sp.addTask(Task("Task 1", 2, 0, False, datetime.date(2017, 1, 1)))
        sp.addTask(Task("Task 2", 2, 0, True, datetime.date(2017, 1, 5)))
        sp.addTask(Task("Task 3", 2, 0, True, datetime.date(2016, 1, 5)))
        p.addSubproject(sp)

        generator = MonthReportGenerator([p])
        generator.setup(2017, 1, 2)
        report = generator.generate()
        self.assertEqual(report.getField("expected_time"), 4)
        self.assertEqual(len(report.getField("to_split")), 0)

    def test_to_split(self):
        p = ScheduleProject("University", (0,0,0), (0,0,0))
        sp = ScheduleSubproject("Calculus")
        sp.addTask(Task("Task 1", 2, 0, False, datetime.date(2017, 1, 1)))
        sp.addTask(Task("Task 2", 20, 0, True, datetime.date(2017, 1, 5)))
        sp.addTask(Task("Task 3", 10, 0, True, datetime.date(2016, 1, 5)))
        p.addSubproject(sp)

        generator = MonthReportGenerator([p])
        generator.setup(2017, 1, 2)
        report = generator.generate()
        self.assertEqual(len(report.getField("to_split")), 1)
