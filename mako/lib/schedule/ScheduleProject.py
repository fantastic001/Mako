
from .ScheduleSubproject import * 
import json

class ScheduleProject(object):
    
    def __init__(self, name, color_bg, color_fg):
        self.name = name 
        self.color_bg = color_bg
        self.color_fg = color_fg 
        self.subprojects = [] 
    
    def __hash__(self):
        return hash(json.dumps(self.toDict(), sort_keys=True))


    def __eq__(self, other):
        return json.dumps(self.toDict(), sort_keys=True) == json.dumps(other.toDict(), sort_keys=True)
    def getName(self):
        return self.name 

    def getBackgroundColor(self):
        return self.color_bg 

    def getForegroundColor(self):
        return self.color_fg 

    def addSubproject(self, sp):
        found = False
        for s in self.subprojects:
            if sp.getName() == s.getName():
                found = True
                break
        if not found:
            self.subprojects.append(sp)

    def getSubprojects(self):
        return self.subprojects 

    def toDict(self):
        d = {}
        d["name"] = self.name
        r,g,b = self.color_bg 
        d["color_bg_r"] = r
        d["color_bg_g"] = g
        d["color_bg_b"] = b
        
        r,g,b = self.color_fg
        d["color_fg_r"] = r
        d["color_fg_g"] = g
        d["color_fg_b"] = b
        d["subprojects"] = []
        for sp in self.subprojects:
            d["subprojects"].append(sp.toDict())
        return d

    def fromDict(d):
        name = d["name"]
        color_bg = (int(d["color_bg_r"]), int(d["color_bg_g"]), int(d["color_bg_b"]))
        color_fg = (int(d["color_fg_r"]), int(d["color_fg_g"]), int(d["color_fg_b"]))
        p = ScheduleProject(name, color_bg, color_fg)
        for sp in d["subprojects"]:
            p.addSubproject(ScheduleSubproject.fromDict(sp))
        return p 
    
    def __repr__(self) -> str:
        return f"ScheduleProject(name = '{self.name}')"
