
class Report(object):
    
    def __init__(self, name, date):
        self.fields = {}
        self.name = name 
        self.date = date

    def getName(self):
        return self.name 

    def getDate(self):
        return self.date

    def setField(self, name, value):
        """
        value can be int, float, string list or dictionary 
        """
        self.fields[name] = value

    def getField(self, name):
        return self.fields.get(name, "")
