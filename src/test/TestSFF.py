
from ..lib.schedule.formats import * 
from ..lib.schedule import * 

import unittest 

from datetime import date 

class TestSFF(unittest.TestCase):
    
    def setUp(self):
        self.projects = [] 
        self.projects.append(ScheduleProject("University", (255, 0, 0), (255, 255, 255)))
        self.projects[-1].addSubproject(ScheduleSubproject("Calculus"))
        self.projects[-1].addSubproject(ScheduleSubproject("Algebra"))
        self.projects[-1].addSubproject(ScheduleSubproject("Computer Science"))

        self.projects.append(ScheduleProject("Community", (0, 255, 0), (255, 255, 255)))
        self.projects[-1].addSubproject(ScheduleSubproject("Milica"))
        self.projects[-1].addSubproject(ScheduleSubproject("Nikola"))

        self.entries = [] 
        self.entries.append(ScheduleEntry(self.projects[0], self.projects[0].getSubprojects()[0], 1,14,4))
        self.entries.append(ScheduleEntry(self.projects[0], self.projects[0].getSubprojects()[0], 4,14,4))
        self.entries.append(ScheduleEntry(self.projects[0], self.projects[0].getSubprojects()[0], 5,14,4))
        self.entries.append(ScheduleEntry(self.projects[1], self.projects[1].getSubprojects()[0], 2,19,4))

    def test_sff(self):
        writer = SFFWriter(self.entries, self.projects, filename="test.sff", day=2, month=5, year=2017)
        writer.write()
        writer.close()

        reader = SFFReader()
        reader.open(filename="test.sff")
        reader.read()
        reader.close()
        self.assertEqual(reader.getDate(), date(2017, 5, 2))
        entries = reader.getEntries()
        projects = reader.getProjects()

        for i in range(len(projects)):
            self.assertEqual(projects[i].getName(), self.projects[i].getName())
            for j in range(len(projects[i].getSubprojects())):
                self.assertEqual(projects[i].getSubprojects()[j].getName(), self.projects[i].getSubprojects()[j].getName())
        for i in range(len(entries)):
            self.assertEqual(entries[i].getProject().getName(), self.entries[i].getProject().getName())
            self.assertEqual(entries[i].getDay(), self.entries[i].getDay())
