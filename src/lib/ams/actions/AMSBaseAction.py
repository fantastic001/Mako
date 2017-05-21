
class AMSBaseAction:
    
    name = "base"
    description = ""

    def __init__(self, description, cfg):
        self.cfg = cfg 
        self.description = description 

    def getDescription(self):
        return self.description 

    def getConfig(self):
        return self.cfg 
    
    def measure(self):
        pass
