
import unittest 

from ..lib.ams.actions import AMSTableEntryCountAction
from ..lib.table import * 

class TestAMSTableEntryCountAction(unittest.TestCase):
    
    def test_basic_counting(self):
        a = AMSTableEntryCountAction("m", "Measures how many entries there are in table test", {
            "table_name": "test"
        })
        table = Table("test", ["a", "b", "c"])
        table.addEntry(["1", "2", "3"])
        table.addEntry(["1", "2", "3"])
        table.addEntry(["1", "2", "3"])
        self.assertEqual(a.measure([table]), 3)
    
    def test_zero(self):
        a = AMSTableEntryCountAction("m", "Measures how many entries there are in table test", {
            "table_name": "test"
        })
        table = Table("wrong_one", ["a", "b", "c"])
        table.addEntry(["1", "2", "3"])
        table.addEntry(["1", "2", "3"])
        table.addEntry(["1", "2", "3"])
        self.assertEqual(a.measure([table]), 0)

    def test_filter(self):
        a = AMSTableEntryCountAction("m", "Measures how many entries there are in table test", {
            "table_name": "test",
            "filter": "1"
        })
        table = Table("test", ["a", "b", "c"])
        table.addEntry(["1", "2", "3"])
        table.addEntry(["5", "2", "3"])
        table.addEntry(["7", "2", "3"])
        self.assertEqual(a.measure([table]), 1)
        
