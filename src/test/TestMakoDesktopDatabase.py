
import unittest 

from ..desktop import MakoDesktopDatabase

import shutil
import os

class TestMakoDesktopDatabase(unittest.TestCase):
    
    def setUp(self):
        self.db = MakoDesktopDatabase(path="test_data/db/desktop/")
        self.db2 = MakoDesktopDatabase(path="test_data/db/desktop2/")
        self.db3 = MakoDesktopDatabase(path="test_data/db/desktop3/")
        for d in [""]:
            f = open("test_data/db/desktop%s/Measurements/Notes size/data.csv" % d, "w")
            f.write("")
            f.close()
        os.makedirs("test_data/empty_dir", exist_ok=True)

        f = open("test_data/db/desktop/Measurements/Notes size/data.csv", "w")
        f.write("01.01.2016.,18.5")
        f.close()
            
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
        self.assertEqual(len(data), len(data2))
    def test_upload_reports(self):
        self.DUD(self.db.downloadReports, self.db2.uploadReports, self.db2.downloadReports)

    def test_schedule_conditions_upload(self):
        self.DUD(self.db.downloadDefaultConditions, self.db2.uploadDefaultConditions, self.db2.downloadDefaultConditions)

    def test_upload_schedules(self):
        self.DUD(self.db.downloadSchedules, self.db2.uploadSchedules, self.db2.downloadSchedules)
        
    def test_upload_tables(self):
        self.DUD(self.db.downloadTables, self.db2.uploadTables, self.db2.downloadTables)

    def test_export(self):
        self.db.export(self.db3)
        projects1 = self.db.downloadProjects()
        projects2 = self.db3.downloadProjects()
        self.assertEqual(len(projects1), len(projects2))
        for i in range(len(projects1)):
            self.assertEqual(projects1[i].getName(), projects2[i].getName())
        self.assertEqual(self.db.downloadMeasurementData("measureNotes"), self.db3.downloadMeasurementData("measureNotes"))
        shutil.rmtree("test_data/db/desktop3/")

    def test_custom_due_dates(self):
        projects = self.db.downloadProjects()
        for project in projects:
            if project.getName() == "Work":
                for subproject in project.getSubprojects():
                    if subproject.getName() == "Google":
                        tasks = subproject.getAllTasks()
                        self.assertEqual(tasks[0].getDueDate().day, 5)
                        self.assertEqual(tasks[0].getDueDate().month, 1)
                        self.assertEqual(tasks[0].getDueDate().year, 2017)
