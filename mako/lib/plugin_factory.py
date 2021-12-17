
from mako.desktop.MakoTaskWarriorDatabase import MakoTaskWarriorDatabase
from mako.desktop.MakoODSDesktopDatabase import MakoODSDesktopDatabase
from mako.desktop.MakoDesktopDatabase import MakoDesktopDatabase
from mako.lib.configuration import Configuration
from mako.lib.database.mako_database import MakoDatabase
import sys 
import mako.lib
from typing import List, Dict
import importlib
import os 
import os.path
class PluginFactory:
    """
    Used to read plugin selection from given configuration and to create database instances and other extensions
    """

    def __init__(self, config: Configuration) -> None:
        self.config = config
        self.search_paths = [
            os.path.abspath(os.path.dirname(os.path.dirname(mako.lib.__path__[0]))),
            *self.config.getProperty("search_paths", [])
        ]
        plugins = [
            "mako.lib.database",
            "mako.desktop",
            *self.config.getProperty("plugins", [])
        ]
        saved_path = sys.path
        self.plugins = {}
        for path in self.search_paths:
            sys.path.append(path)
        for name in plugins:
            self.plugins[name] = importlib.import_module(name)
        sys.path = saved_path
        
    
    def getDatabaseInstance(self) -> MakoDatabase:
        for cls in self.getDatabaseClasses():
            if cls.__name__ == self.config.getProperty("database", "MakoDesktopDatabase"):
                return cls(**self.config.getProperty("database_properties", {
                    "path": os.path.join(os.environ["HOME"], ".mako", "db"),
                    "autosave": True
                }))
    def getDatabaseClasses(self):
        databases: Dict = dict(
            MakoDesktopDatabase = "mako.desktop",
            MakoMemoryDatabase = "mako.lib.database",
            MakoODSDesktopDatabase = "mako.desktop",
            MakoTaskWarriorDatabase = "mako.desktop",
            **self.config.getProperty("databases", {})
        )
        result = [] 
        for name, module in databases.items():
            result.append(getattr(self.plugins[module], name))
        return result
    
    def getSecondaryDatabaseInstances(self):
        result = []
        secondary: Dict[str, dict] = self.config.getProperty("secondary_databases", {
            "taskwarrior": {
                "class_name": "MakoTaskWarriorDatabase",
                "path": os.path.join(os.environ["HOME"], ".taskwarrior")
            }
        })
        for name, params in secondary.items():
            found = False
            for cls in self.getDatabaseClasses():
                if cls.__name__ == params["class_name"]:
                    del params["class_name"]
                    result.append((name, cls(**params)))
                    found = True
            if not found:
                raise ValueError("Cannot find suitable class for secondary database %s" % name)
        return result