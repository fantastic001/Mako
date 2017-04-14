
from ..lib.schedule import ScheduleSubproject
from ..lib.schedule import Task 
import unittest
import datetime

class TestScheduleSubproject(unittest.TestCase):

    def test_basic(self):
        sp = ScheduleSubproject("Calculus")
        self.assertEqual(sp.getName(), "Calculus")

    def test_tasks(self):
        sp = ScheduleSubproject("Calculus")
        sp.addTask(Task("Task 1", 2, 0, False, datetime.date.today() - datetime.timedelta(days=5)))
        sp.addTask(Task("Task 1", 2, 0, True, datetime.date.today() - datetime.timedelta(days=5)))
        self.assertEqual(len(sp.getUndoneTasksDueThisMonth()), 1)
        sp.getUndoneTasks()[0].setDone()
        self.assertEqual(len(sp.getUndoneTasks()), 0)
