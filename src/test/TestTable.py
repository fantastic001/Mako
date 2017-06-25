
import unittest 

from ..lib.table import * 

class TestTable(unittest.TestCase): 
    
    def setUp(self):
        self.table = Table("test", ["a", "b", "c"])

    def test_creation(self):
        table = Table("test", ["a", "b"])
        self.assertEqual(table.getName(), "test")
        self.assertEqual(table.getFields(), ["a", "b"])

    def test_entry_addition(self):
        self.table.addEntry(["a", "b", "c"])
        self.assertEqual(self.table.getEntries(), [["a", "b", "c"]])
        self.assertEqual(self.table.getEntryCount(), 1)

    def test_entry_removal(self):
        self.table.addEntry(["a", "b", "c"])
        self.table.removeEntry(1)
        self.assertEqual(len(self.table.getEntries()), 0)

    def test_search(self):
        self.table.addEntry(["a", "b", "c"])
        self.assertEqual(self.table.getEntries("a"), [["a", "b", "c"]])
        self.assertEqual(self.table.getEntries("d"), [])

    def test_entry_update(self):
        self.table.addEntry(["a", "b", "c"])
        self.assertEqual(self.table.getEntries(), [["a", "b", "c"]])
        self.table.updateEntry(1, ["a", "b", "d"])
        self.assertEqual(self.table.getEntries(), [["a", "b", "d"]])

    def test_to_dict(self):
        self.table.addEntry(["a", "b", "c"])
        d = self.table.toDict()
        self.assertEqual(d["name"], "test")
        self.assertEqual(d["fields"], ["a", "b", "c"])
        self.assertEqual(len(d["entries"]), 1)

    def test_from_dict(self): 
        self.table.addEntry(["a", "b", "c"])
        d = self.table.toDict()
        table = Table.fromDict(d)
        self.assertEqual(table.getName(), "test")
