
import unittest 

from ..lib.ams.actions import AMSDirectorySizeAction

class TestAMSDirectorySizeAction(unittest.TestCase):
    
    def test_empty(self):
        a = AMSDirectorySizeAction({
            "path": "test_data/empty_dir"
        })
        self.assertEqual(a.measure(), 0)
    
