
from .lib.configuration import * 
from .lib.MemoryConfiguration import * 
from .lib.database import *
from mako.desktop import *


class MakoDatabaseFactory(object):
    def __init__(self, configuration: Configuration):
        self.configuration: Configuration = configuration
    def getDatabase(self) -> MakoDatabase: 
        params = self.configuration.getProperty("params", {})
        db = self.configuration.getProperty("database", "")        
        if db == "desktop": return MakoDesktopDatabase(**params)
        elif db == "memory": 
            memoryConfiguration = MemoryConfiguration({
                "database": params.get("db", "taskwarrior"),
                "params": params.get("params", {})
            })
            if memoryConfiguration.getProperty("database", "taskwarrior") == "taskwarrior":
                if "path" not in memoryConfiguration.getProperty("params", {}):
                    memoryConfiguration.getProperty("params", {})["path"] = "./test_data/db/task/"
            if "db" in params: del params["db"] 
            factory = MakoDatabaseFactory(memoryConfiguration)
            return MakoMemoryDatabase(db = factory.getDatabase(), **params)
        elif db == "taskwarrior": return MakoTaskWarriorDatabase(**params)
        else:
            return MakoDatabase()
