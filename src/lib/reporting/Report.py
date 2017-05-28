
import json 
import datetime

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

    def fromJSON(self, json_data):
        data = json.loads(json_data)
        if "date" in data.keys():
            self.date = datetime.datetime.strptime(data["date"], "%Y-%m-%d")
        if "name" in data.keys():
            self.name = data["name"]
        self.fields = data 

    def toJSON(self):
        d = self.fields
        d["date"] = datetime.datetime.strftime(self.date, "%Y-%m-%d")
        d["name"] = self.name 
        return json.dumps(d, indent=4)
