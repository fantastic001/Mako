
import datetime 

from .ScheduleProject import * 
from .ScheduleSubproject import * 
from .ScheduleEntry import * 
from .ScheduleCondition import * 

class Schedule(object):

    def __init__(self, date):
        self.date = date 
        self.entries = [] 
        self.conditions = [] 

    def addCondition(self, cond):
        self.conditions.append(cond)

    def getConditions(self):
        return self.conditions

    def check(self):
        """
        Returns list of pairs where first element is entry and second is condition 
        """
        res = []
        for cond in self.getConditions():
            for entry in self.entries:
                if not cond.check(self.getDate(), entry):
                    res.append((entry, cond))
        return res

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
        d["conditions"] = []
        for cond in self.conditions:
            d["conditions"].append(cond.toDict())
        return d 

    def fromDict(d):
        
        date = datetime.datetime.strptime(d["date"], "%Y-%m-%d")
        s = Schedule(date)
        for e in d["entries"]:
            s.addEntry(ScheduleEntry.fromDict(e))
        for c in d["conditions"]:
            s.addCondition(ScheduleCondition.fromDict(c))
        return s
