
import unittest 
from ..lib.ams import * 
from ..lib.schedule import * 

class TestAMS(unittest.TestCase):
    
    def test_appending(self):
        ams = AMS("test_data/db/")
        project = ScheduleProject("Notes", (0,0,0), (0,0,0,))
        subproject = ScheduleSubproject("Size")
        m = ams.measure(project, subproject)
        self.assertEqual(len(m), 3)
        ams.append(project, subproject, m)
