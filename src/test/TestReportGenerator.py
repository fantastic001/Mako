
import unittest 

from ..lib.reporting import ReportGenerator
from ..lib.reporting import Report


import datetime 

class DummyReportGenerator(ReportGenerator):
    def generate(self):
        r = Report("test", datetime.date.today())
        r.setField("a", 1)
        return r

class TestReportGenerator(unittest.TestCase):
    
    def test_basic(self):
        projects = [] 
        generator = DummyReportGenerator([])
        r = generator.generate()
        self.assertEqual(r.getField("a"), 1)
        self.assertEqual(r.getField("b"), "")
        self.assertEqual(generator.getProjects(), [])
