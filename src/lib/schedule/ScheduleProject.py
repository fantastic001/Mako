
class ScheduleProject(object):
    
    def __init__(self, name, color_bg, color_fg):
        self.name = name 
        self.color_bg = color_bg
        self.color_fg = color_fg 
        self.subprojects = [] 

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



