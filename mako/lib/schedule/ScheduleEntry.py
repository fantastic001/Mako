
from .ScheduleProject import * 
import json 

class ScheduleEntry(object):
    
    def __init__(self, project, subproject, day, start, duration):
        self.project = project 
        self.subproject = subproject 
        self.day = day 
        self.start = start 
        self.duration = duration 

    def getProject(self):
        return self.project 
    
    def __hash__(self):
        return hash(json.dumps(self.toDict(), sort_keys=True))

    def __eq__(self, other):
        if other is None:
            return False
        return json.dumps(self.toDict(), sort_keys=True) == json.dumps(other.toDict(), sort_keys=True)

    def getSubproject(self):
        return self.subproject

    def getDay(self):
        return self.day

    def getStart(self):
        return self.start 

    def getDuration(self):
        return self.duration 

    def toDict(self):
        d = {}
        d["project"] = self.project.toDict()
        d["subproject"] = self.subproject.toDict()
        d["day"] = self.day
        d["start"] = self.start 
        d["duration"] = self.duration 
        return d 

    def fromDict(d):
        proj = ScheduleProject.fromDict(d["project"])
        sp = ScheduleSubproject.fromDict(d["subproject"])
        day = int(d["day"])
        start = int(d["start"])
        duration = int(d["duration"])
        return ScheduleEntry(proj, sp, day, start, duration)
