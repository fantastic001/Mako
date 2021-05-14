
import unittest 

from ..lib.database import MakoMemoryDatabase 
from ..lib.schedule import * 
from ..lib.reporting import * 
from ..lib.table import * 
from ..lib import MakoCRUD

import datetime

class TestMakoCRUD(unittest.TestCase):

    def setUp(self):
        self.db = MakoMemoryDatabase()
        p1 = ScheduleProject("a", (0,0,0), (0,0,0))
        sp1 = ScheduleSubproject("a/a")
        sp1.addTask(Task("task1", expected=2, due=datetime.date(2017, 5, 2)))
        sp1.addTask(Task("task2", expected=2, due=datetime.date(2017, 5, 2)))
        p1.addSubproject(sp1)
        self.db.uploadProjects([p1])

        schedule = Schedule(datetime.date.today())
        schedule.addEntry(ScheduleEntry(p1, sp1, 2, 11, 4))
        self.db.uploadSchedules([schedule])

        table = Table("t1", ["a", "b", "c"])
        table.addEntry(["1", "2", "3"])
        self.db.uploadTables([table])

        self.crud = MakoCRUD(self.db)

    def test_add_project(self):
        self.crud.addProject("ahhh")
        self.assertEqual(len(self.db.downloadProjects()), 2)

    def test_visit_projects(self):
        l = []
        self.crud.visitProjects(lambda p: l.append(p))
        self.assertEqual(len(l), 1)

    def test_delete_projects(self):
        self.crud.deleteProject("a")
        self.assertEqual(len(self.db.downloadProjects()), 0)

    def test_visit_subprojects(self):
        l = []
        self.visitSubprojects("a", lambda x: l.append(x))
        self.assertEqual(len(l), 1)

    def test_add_subproject(self):
        self.crud.addSubproject("a", "a/b")
        self.assertEqual(len(self.db.downloadProjects()[0].getSubprojects()), 2)



