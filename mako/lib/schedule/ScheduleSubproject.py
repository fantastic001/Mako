
import datetime

from .Task import * 
import json

class ScheduleSubproject(object):

    def __init__(self, name, fields = None):
        self.name = name 
        if fields is None:
            self.fields = {}
        self.tasks = [] 
        self.active = True
    
    def __hash__(self):
        return hash(json.dumps(self.toDict(), sort_keys=True))


    def __eq__(self, other):
        if other is None: return False
        return json.dumps(self.toDict(), sort_keys=True) == json.dumps(other.toDict(), sort_keys=True)
    def setActive(self, active=True):
        """
        Sets if subproject is active. If set to False, subproject is not considered in processing. It is like removal but only logically (it is still considered when generating reports).
        """
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
        d["fields"] = dict(**self.fields)
        for task in self.tasks:
            d["tasks"].append(task.toDict())
        return d

    def fromDict(d):
        sp = ScheduleSubproject(d["name"], dict(**d["fields"]))
        sp.setActive(d.get("active", True))
        for task in d["tasks"]:
            sp.addTask(Task.fromDict(task))
        return sp 
    
    def setField(self, fields_name, fields_value):
        self.fields[fields_name] = fields_value
    
    def hasField(self, field_name) -> bool:
        return field_name in self.fields
    
    def getField(self, field_name):
        if self.hasField(field_name):
            return self.fields[field_name]
        else:
            return None
    def getFieldList(self):
        return list(self.fields.keys())
