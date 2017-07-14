
import json
import os

class ConfigManager(object):
    
    def __init__(self, path, intime=True):
        self.path = path 
        self.intime = intime
        self.params = {}
        if os.path.exists(self.path):
            f = open(self.path, "r")
            self.params = json.loads(f.read())
            f.close()
    def save(self):
        f = open(self.path, "w")
        f.write(json.dumps(self.params))
        f.close()

    def setParam(self, k, v):
        self.params[k]=v
        if self.intime:
            self.save()

    def getParam(self, k, default):
        return self.params.get(k, default)
        
        
