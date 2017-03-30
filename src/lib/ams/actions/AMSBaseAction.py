
class AMSBaseAction:
    
    name = "base"

    def __init__(self, cfg):
        self.cfg = cfg 

    def getConfig(self):
        return self.cfg 
    
    def measure(self):
        pass
