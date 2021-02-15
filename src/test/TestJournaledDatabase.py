
import unittest 
from ..lib.database import * 
from ..lib.database import *

class MockJournal(Journal):
    def __init__(self):
        self.data = []
        self.registered = True
        self.marked = True
    def commit(self, data):
        self.data.append(data)
        self.registered = False
        self.marked = False
    def register(self):
        self.registered = True
    def mark(self):
        self.marked  = True
    def getLast(self):
        return self.data[-1]
    def isMarked(self):
        return self.marked
    def isRegistered(self):
        return self.registered


class MockMakoDatabase(MakoDatabase):
    def init(self):
        self.uploadedProjectsCount = 0 

    def validate(self):
        pass

    def uploadProjects(self, projects):
        self.uploadedProjectsCount += 1 

    def uploadMeasurementActions(self, actions):
        pass

    def uploadMeasurementData(self, action_id, data):
        pass

    def uploadData(self, data):
        pass

    def uploadSchedules(self, schedules):
        pass

    def uploadReports(self, reports):
        pass

    def uploadDefaultConditions(self, conditions):
        pass

    def uploadTables(self, tables):
        pass

    def downloadProjects(self):
        return []

    def downloadMeasurementActions(self):
        return []

    def downloadMeasurementData(self, action_id):
        return [] 

    def downloadData(self):
        return [] 

    def downloadSchedules(self):
        return [] 

    def downloadReports(self):
        return [] 

    def downloadDefaultConditions(self):
        return [] 

    def downloadTables(self):
        return [] 

class TestJournaledDatabase(unittest.TestCase):
    
    def setUp(self):
        self.journal = MockJournal()

    def test_creation(self):
        db = JournaledDatabase(db=MockMakoDatabase(), journal=self.journal)
        self.assertIsInstance(db, MakoDatabase)
    
    def test_upload_operation_commits(self):
        db = JournaledDatabase(db=MockMakoDatabase(), journal=self.journal)
        db.uploadProjects([])
        self.assertEqual(len(self.journal.data), 1)
    
    def test_downloading_data_does_not_commit(self):
        db = JournaledDatabase(db=MockMakoDatabase(), journal=self.journal)
        projects = db.downloadProjects()
        self.assertEqual(len(self.journal.data), 0)
    
    def test_journaled_database_behaves_like_mako_database(self):
        db = JournaledDatabase(db=MockMakoDatabase(), journal=self.journal, x=5)
        self.assertEqual(db.getParams()["x"], 5)
    
    def test_all_uploads_will_commit(self):
        db = JournaledDatabase(db=MockMakoDatabase(), journal=self.journal)
        count = 0
        for attr in dir(db):
            if attr.startswith("upload") and attr != "uploadMeasurementData":
                getattr(db, attr)([])
                count += 1 
        db.uploadMeasurementData("x", [])
        self.assertEqual(count+1, len(self.journal.data))
    
    def test_commits_are_actual_database(self):
        db = JournaledDatabase(db=MockMakoDatabase(), journal=self.journal)
        db.uploadProjects([])
        self.assertEqual(self.journal.getLast()["projects"], [])
    
    def test_registered_but_not_marked(self):
        db = JournaledDatabase(db=MockMakoDatabase(), journal=self.journal)
        db.uploadProjects([])
        self.journal.registered = True
        self.journal.marked = False
        mock = MockMakoDatabase()
        db = JournaledDatabase(db=mock, journal=self.journal)
        self.assertEqual(mock.uploadedProjectsCount, 1)
    
    def test_unregistered_journal_not_commited(self):
        self.journal.registered = False
        self.journal.marked = False
        mock = MockMakoDatabase()
        db = JournaledDatabase(db=mock, journal=self.journal)
        self.assertEqual(mock.uploadedProjectsCount, 0)