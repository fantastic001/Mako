
import unittest 

from ..desktop import MakoDesktopDatabase

class TestMakoDesktopDatabase(unittest.TestCase):
    
    def setUp(self):
        self.db = MakoDesktopDatabase(path="test_data/db/desktop/")
        self.db2 = MakoDesktopDatabase(path="test_data/db/desktop2/")
        
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

    def DUD(self, d, u, d2):
        a = d()
        u(a)
        b = d2()
        self.assertEqual(len(a), len(b))



    def test_project_upload(self):
        self.DUD(self.db.downloadProjects, self.db2.uploadProjects, self.db2.downloadProjects)
    
    def test_measurement_actions_upload(self):
        self.DUD(self.db.downloadMeasurementActions, self.db2.uploadMeasurementActions, self.db2.downloadMeasurementActions)

    def test_measurement_data_upload(self):
        data = self.db.downloadMeasurementData("measureNotes")
        self.db2.uploadMeasurementData("measureNotes", data)
        data2 = self.db2.downloadMeasurementData("measureNotes")
        self.assertEqual(len(data), len(data2)+1)
    def test_upload_reports(self):
        self.DUD(self.db.downloadReports, self.db2.uploadReports, self.db2.downloadReports)

    def test_schedule_conditions_upload(self):
        self.DUD(self.db.downloadDefaultConditions, self.db2.uploadDefaultConditions, self.db2.downloadDefaultConditions)

    def test_upload_schedules(self):
        self.DUD(self.db.downloadSchedules, self.db2.uploadSchedules, self.db2.downloadSchedules)
        
    def test_upload_tables(self):
        self.DUD(self.db.downloadTables, self.db2.uploadTables, self.db2.downloadTables)
