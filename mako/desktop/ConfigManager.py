
import json
import os
from ..lib import Configuration

class ConfigManager(Configuration):
    def __init__(self, path, intime=True):
        """
        Initialize coonfiguration object for using DesktopDatabase 
        
        if file already exists, parameters of config are loaded. 

        Args:
            path: path of config file to save to 
            intime: if True, setParam function will always save it to config file, if False, call to save is expected to write to file
        """
        self.path = path 
        self.intime = intime
        self.params = {}
        if os.path.exists(self.path):
            f = open(self.path, "r")
            self.params = json.loads(f.read())
            f.close()
    def open(self) -> dict:
        return self.params
    
    def save(self, params):
        self.params = params
        if self.intime:
            self.saveToFile(params)

    def saveToFile(self, params: dict):
        f = open(self.path, "w")
        f.write(json.dumps(params))
        f.close()
