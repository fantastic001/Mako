
from ..lib.schedule import ScheduleEntry , ScheduleProject, ScheduleSubproject

import unittest 


class TestScheduleEntry(unittest.TestCase):
    
    def test_creation(self):
        p = ScheduleProject("University", (255, 0, 0), (255,255,255))
        sp = ScheduleSubproject("Calculus")
        p.addSubproject(sp)
        e = ScheduleEntry(p, sp, 1, 14, 4)
        self.assertEqual(e.getProject().getName(), "University")
        self.assertEqual(e.getSubproject().getName(), "Calculus")
        self.assertEqual(e.getDay(), 1)
        self.assertEqual(e.getStart(), 14)
        self.assertEqual(e.getDuration(), 4)

