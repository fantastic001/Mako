
import datetime

from .Task import * 
import json

class ScheduleSubproject(object):

    def __init__(self, name):
        self.name = name 
        self.tasks = [] 
        self.active = True
    
    def __hash__(self):
        return hash(json.dumps(self.toDict(), sort_keys=True))


    def __eq__(self, other):
        if other is None: return False
        return json.dumps(self.toDict(), sort_keys=True) == json.dumps(other.toDict(), sort_keys=True)
    def setActive(self, active=True):
        self.active = active

    def isActive(self):
        return self.active

    def getName(self):
        return self.name 

    def addTask(self, task):
        self.tasks.append(task)

    def getAllTasks(self):
        return self.tasks

    def getUndoneTasks(self):
        res = [] 
        for t in self.tasks:
            if not t.isDone():
                res.append(t)
        return res

    def getUndoneTasksDueThisMonth(self):
        res = [] 
        today = datetime.date.today()
        for t in self.tasks:
            if not t.isDone() and (t.getDueDate() - today).days < 31:
                res.append(t)
        return res

    def deleteAllTasks(self):
        self.tasks = []

    def toDict(self):
        d = {}
        d["name"] = self.name
        d["active"] = self.active
        d["tasks"] = []
        for task in self.tasks:
            d["tasks"].append(task.toDict())
        return d

    def fromDict(d):
        sp = ScheduleSubproject(d["name"])
        sp.setActive(d.get("active", True))
        for task in d["tasks"]:
            sp.addTask(Task.fromDict(task))
        return sp 
