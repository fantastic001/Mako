
from ..lib.schedule import ScheduleProject, ScheduleSubproject
import unittest 

class TestScheduleProject(unittest.TestCase):
    
    def test_basic(self):
        proj = ScheduleProject("University", (255, 0, 120), (255, 250, 0))
        self.assertEqual(proj.getName(), "University")
        self.assertEqual(proj.getBackgroundColor(), (255, 0, 120))
        self.assertEqual(proj.getForegroundColor(), (255, 250, 0))


    def test_subprojects(self):
        proj = ScheduleProject("University", (255, 0, 120), (255, 250, 0))
        self.assertEqual(len(proj.getSubprojects()), 0)
        proj.addSubproject(ScheduleSubproject("Calculus"))
        self.assertEqual(len(proj.getSubprojects()), 1)
        self.assertEqual(proj.getSubprojects()[0].getName(), "Calculus")
        proj.addSubproject(ScheduleSubproject("Calculus"))
        self.assertEqual(len(proj.getSubprojects()), 1)
        proj.addSubproject(ScheduleSubproject("Calculus 2"))
        self.assertEqual(len(proj.getSubprojects()), 2)
