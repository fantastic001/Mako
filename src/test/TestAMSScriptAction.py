
import unittest 

from ..lib.ams.actions import AMSScriptAction
import os

class TestAMSScriptAction(unittest.TestCase):
    
    def test_stdout(self):
        a = AMSScriptAction({
            "path": "./test_data/scripts/test.sh",
            "interpreter": "sh"
        })
        self.assertEqual(a.measure(), 5.0)
    
    def test_stdout_with_args(self):
        a = AMSScriptAction({
            "path": "./test_data/scripts/test2.sh",
            "interpreter": "sh",
            "args": "5",
        })
        self.assertEqual(a.measure(), 5.0)
    
    def test_file_with_args(self):
        a = AMSScriptAction({
            "path": "./test_data/scripts/test3.sh",
            "interpreter": "sh",
            "args": "/tmp/myfile",
            "result_as": "/tmp/myfile"
        })
        self.assertEqual(a.measure(), 5.0)
