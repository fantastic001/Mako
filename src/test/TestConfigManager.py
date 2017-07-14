
from ..desktop import ConfigManager 
import unittest

class TestConfigManager(unittest.TestCase):
    
    def setUp(self):
        self.c = ConfigManager("test_data/cfg.json")

    def test_intime(self):
        self.c.setParam("a", 5)
        cfg = ConfigManager("test_data/cfg.json")
        self.assertEqual(cfg.getParam("a", 5000), 5)

    def test_no_intime(self):
        cfg = ConfigManager("test_data/cfg.json", intime=False)
        cfg.setParam("a", 10)
        cfg = ConfigManager("test_data/cfg.json")
        a=cfg.getParam("a", 0)
        self.assertEqual(a, 5)
