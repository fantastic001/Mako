
import json

class AMSBaseAction:
    
    name = "base"
    description = ""
    identifier = "" # identifies specific action in database

    def __init__(self, identifier, description, cfg):
        self.cfg = cfg 
        self.description = description 
        self.identifier = identifier 
    
    def __hash__(self):
        return hash(json.dumps(self.toDict(), sort_keys=True))

    def getIdentifier(self):
        return self.identifier 

    def getDescription(self):
        return self.description 

    def getConfig(self):
        return self.cfg 
    
    def measure(self, tables):
        pass

    def toDict(self):
        data = self.getConfig()
        data["id"] = self.getIdentifier()
        data["action"] = self.name
        data["description"] = self.getDescription()
        return data
