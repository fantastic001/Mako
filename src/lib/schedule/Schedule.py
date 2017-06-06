
import datetime 

from .ScheduleProject import * 
from .ScheduleSubproject import * 
from .ScheduleEntry import * 

class Schedule(object):

    def __init__(self, date):
        self.date = date 
        self.entries = [] 

    def addEntry(self, entry):
        self.entries.append(entry)

    def getEntries(self):
        return self.entries 

    def getDate(self):
        return self.date

    def toDict(self):
        d = {}
        d["date"] = datetime.datetime.strftime(self.date, "%Y-%m-%d")
        d["entries"] = []
        for e in self.entries:
            d["entries"].append(e.toDict())
        return d 

    def fromDict(d):
        
        date = datetime.datetime.strptime(d["date"], "%Y-%m-%d")
        s = Schedule(date)
        for e in d["entries"]:
            s.addEntry(ScheduleEntry.fromDict(e))
        return s
