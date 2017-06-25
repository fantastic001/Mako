
import unittest 
from ..lib.ams import * 
from ..lib.schedule import * 

import json 

class TestAMS(unittest.TestCase):
    
    def test_appending(self):
        fname = "test_data/db/Notes/Size/measure.json"
        project = ScheduleProject("Notes", (0,0,0), (0,0,0,))
        subproject = ScheduleSubproject("Size")
        ams = AMS()
        f = open(fname)
        m = ams.measure(project, subproject, [], json.loads(f.read())["measurings"])
        f.close()
        self.assertEqual(len(m), 3)
