
class Report(object):
    
    def __init__(self):
        self.fields = {}

    def setField(self, name, value):
        """
        value can be int, float, string list or dictionary 
        """
        self.fields[name] = value

    def getField(self, name):
        return self.fields.get(name, "")
