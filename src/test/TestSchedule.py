
import unittest 

from ..lib.schedule import * 

import datetime 

class TestSchedule(unittest.TestCase):
    
    def setUp(self):
        self.schedule = Schedule(date=datetime.date.today())
        self.schedule.addEntry(ScheduleEntry(
            project=ScheduleProject("Project 1", (255,255,255), (0,0,0)), 
            subproject=ScheduleSubproject("Subproject 1"), 
            day=2, 
            start=14, 
            duration=3))

    def test_add_entry(self):
        self.schedule.addEntry(ScheduleEntry(
            project=ScheduleProject("Project 1", (255,255,255), (0,0,0)),
            subproject=ScheduleSubproject("Subproject 1"),
            day=4,
            start=14,
            duration=3))
        self.assertEqual(len(self.schedule.getEntries()), 2)

    def test_entry_remove(self):
        self.schedule.removeEntry(2, 14, 5)
        self.assertEqual(len(self.schedule.getEntries()), 0)
    
    def test_tasks_today(self):
        p1 = ScheduleProject("a", (0,0,0), (0,0,0))
        sp1 = ScheduleSubproject("a/a")
        sp1.addTask(Task("task1", expected=2, due=datetime.date(2017, 5, 2)))
        sp1.addTask(Task("task2", expected=2, due=datetime.date(2017, 5, 2)))
        p1.addSubproject(sp1)

        schedule = Schedule(datetime.date.today())
        schedule.addEntry(ScheduleEntry(p1, sp1, 2, 11, 4))
        today = schedule.tasksToday([p1], 2)
        self.assertEqual(today[0][2].getText(), "task1")
        self.assertEqual(today[1][2].getText(), "task2")
