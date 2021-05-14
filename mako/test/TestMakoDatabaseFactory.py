
import unittest 

from mako.lib.Configuration import * 
from .. import MakoDatabaseFactory
from mako.lib.database import * 
from mako.desktop.MakoDesktopDatabase import * 
from mako.desktop.MakoTaskWarriorDatabase import * 

class MockConfiguration(Configuration):
    def __init__(self):
        self.numberofOpens = 0 
        self.numberOfSaves = 0 
        self.data = {}
    def save(self, params: dict):
        self.numberOfSaves += 1
        self.data = params
    def open(self) -> dict:
        self.numberofOpens += 1
        return self.data

class TestMakoDatabaseFactory(unittest.TestCase):   
    def setUp(self):
        self.configuration = MockConfiguration()

    def test_creation(self):
        factory = MakoDatabaseFactory(self.configuration)
    
    def test_configuration_not_opened_on_creation(self):
        factory = MakoDatabaseFactory(self.configuration)
        self.assertEqual(self.configuration.numberofOpens, 0)
    
    def test_getting_database_opens_configuration(self):
        factory = MakoDatabaseFactory(self.configuration)
        db = factory.getDatabase()
        self.assertEqual(self.configuration.numberofOpens, 2)
    
    def test_get_database_returns_instance_of_mako_database(self):
        factory = MakoDatabaseFactory(self.configuration)
        db = factory.getDatabase()
        self.assertIsInstance(db, MakoDatabase)
    
    def test_return_desktop_database(self):
        self.configuration.data["database"] = "desktop"
        self.configuration.data["params"] = {
            "path": "./test_data/db/desktop"
        }
        factory = MakoDatabaseFactory(self.configuration)
        db = factory.getDatabase()
        self.assertIsInstance(db, MakoDesktopDatabase)
        self.assertEqual(db.getParams()["path"], "./test_data/db/desktop")

    def test_return_memory_database(self):
        self.configuration.data["database"] = "memory"
        self.configuration.data["params"] = {
            "db": "taskwarrior",
            "frequency": 0, 
            "params": {
                "path": "./test_data/db/task"
            }
        }
        factory = MakoDatabaseFactory(self.configuration)
        db = factory.getDatabase()
        self.assertIsInstance(db, MakoMemoryDatabase)
        self.assertIsInstance(db.getParams()["db"], MakoTaskWarriorDatabase)
    
    def test_return_task_warrior_db(self):
        self.configuration.data["database"] = "taskwarrior"
        factory = MakoDatabaseFactory(self.configuration)
        db = factory.getDatabase()
        self.assertIsInstance(db, MakoTaskWarriorDatabase)
    
    def test_params_passed_to_database(self):
        self.configuration.data["database"] = "memory"
        self.configuration.data["params"] = {
            "random": 5
        }
        factory = MakoDatabaseFactory(self.configuration)
        db = factory.getDatabase()
        self.assertIn("random", db.getParams().keys())
    