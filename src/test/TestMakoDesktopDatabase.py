
import unittest 

from ..desktop import MakoDesktopDatabase

class TestMakoDesktopDatabase(unittest.TestCase):
    
    def setUp(self):
        self.db = MakoDesktopDatabase("test_data/db/desktop/")
        
    def test_project_download(self):
        projects = self.db.downloadProjects()
        self.assertEqual(len(projects), 3)
        c = 0
        for p in projects:
            c += len(p.getSubprojects())
        self.assertEqual(c, 11)

    def test_measurement_actions_download(self):
        metrics = self.db.downloadMeasurementActions()
        self.assertEqual(len(metrics), 1)

    def test_measurement_data_download(self):
        data = self.db.downloadMeasurementData("measureNotes")
        self.assertGreater(len(data), 0)

    def test_download_reports(self):
        a = self.db.downloadReports()
        self.assertEqual(len(a), 3)

    def test_schedule_conditions(self):
        a = self.db.downloadDefaultConditions()
        self.assertEqual(len(a), 1)

    def test_download_schedules(self):
        a = self.db.downloadSchedules()
        self.assertEqual(len(a), 1)
        
    def test_download_tables(self):
        a = self.db.downloadTables()
        self.assertEqual(len(a), 1)
