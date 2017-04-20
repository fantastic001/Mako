
import unittest 

from ..lib.reporting import Report

class TestReport(unittest.TestCase):
    
    def test_basic(self):
        report = Report()
        report.setField("a", 1)
        report.setField("b", 0.75)
        report.setField("c", "c")
        report.setField("d", [1, 2, 3])
        report.setField("e", {"a": "b"})

        self.assertEqual(report.getField("a"), 1)
        self.assertEqual(report.getField("b"), 0.75)
        self.assertEqual(report.getField("c"), "c")
        self.assertEqual(report.getField("d"), [1, 2, 3])
        self.assertEqual(report.getField("e"), {"a": "b"})
        self.assertEqual(report.getField("f"), "")
