
import unittest 

from ..lib.reporting import ReportView
from ..lib.reporting import Report

import datetime 

class DummyReportView(ReportView):
    def show(self, r):
        if r.getField("a") == "a":
            self.display = "a is there"
        else:
            self.display = "a is not there"

class TestReportView(unittest.TestCase):
    
    def test_basic(self):
        r1 = Report("r1", datetime.date.today())
        r1.setField("a", "a")

        r2 = Report("r2", datetime.date.today())
        r2.setField("a", "b")

        r3 = Report("r3", datetime.date.today())
        r3.setField("a", "")

        view = DummyReportView()
        
        view.show(r1)
        self.assertEqual(view.display, "a is there")

        view.show(r2)
        self.assertEqual(view.display, "a is not there")

        view.show(r3)
        self.assertEqual(view.display, "a is not there")
