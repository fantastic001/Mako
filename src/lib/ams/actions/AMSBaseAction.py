
class AMSBaseAction:
    
    name = ""

    def __init__(self, cfg):
        self.cfg = cfg 

    def getConfig(self):
        return self.cfg 
    
    def measure(self):
        pass
