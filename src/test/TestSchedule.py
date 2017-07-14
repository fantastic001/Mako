
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
        
