
import unittest 

from ..lib.database import *
from ..lib.schedule import * 

class DummyDatabase(MakoDatabase):
    
    def init(self):
        self.initialized = True 
        self.p = []

    def validate(self):
        return False

    def uploadProjects(self, projects):
        self.p = [] 
        for p in projects:
            self.p.append(p)

    def downloadProjects(self):
        return self.p

    def downloadMeasurementData(self, a):
        return []

    def downloadMeasurementActions(self):
        return []

    def downloadReports(self):
        return []

    def downloadSchedules(self):
        return []

    def downloadDefaultConditions(self):
        return [] 

    def downloadTables(self):
        return []
    def downloadData(self):
        return []

class TestMakoMemoryDatabase(unittest.TestCase):
    
    def test_frequency_zero(self):
        dummy = DummyDatabase()
        mem = MakoMemoryDatabase(frequency=0, db=dummy)
        mem.uploadProjects([ScheduleProject("A", (0,0,0), (0,0,0))])
        self.assertEqual(dummy.downloadProjects()[0].getName(), "A")
    
    def test_frequency_non_zero(self):
        dummy = DummyDatabase()
        mem = MakoMemoryDatabase(frequency=10, db=dummy)
        if not mem.validate():
            mem.init()
        mem.uploadProjects([ScheduleProject("A", (0,0,0), (0,0,0))])
        self.assertEqual(len(dummy.downloadProjects()),0)
        mem.uploadProjects([ScheduleProject("A", (0,0,0), (0,0,0))])
        mem.uploadProjects([ScheduleProject("A", (0,0,0), (0,0,0))])
        mem.uploadProjects([ScheduleProject("A", (0,0,0), (0,0,0))])
        mem.uploadProjects([ScheduleProject("A", (0,0,0), (0,0,0))])
        mem.uploadProjects([ScheduleProject("A", (0,0,0), (0,0,0))])
        mem.uploadProjects([ScheduleProject("A", (0,0,0), (0,0,0))])
        mem.uploadProjects([ScheduleProject("A", (0,0,0), (0,0,0))])
        mem.uploadProjects([ScheduleProject("A", (0,0,0), (0,0,0))])
        mem.uploadProjects([ScheduleProject("A", (0,0,0), (0,0,0))])
        self.assertEqual(dummy.downloadProjects()[0].getName(), "A")
