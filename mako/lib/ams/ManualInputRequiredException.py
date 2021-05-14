
class ManualInputRequiredException(Exception):
    
    def __init__(self, msg):
        self.msg = msg 

    def message(self):
        return self.msg
