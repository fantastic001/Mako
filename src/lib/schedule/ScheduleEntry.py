

class ScheduleEntry(object):
    
    def __init__(self, project, subproject, day, start, duration):
        self.project = project 
        self.subproject = subproject 
        self.day = day 
        self.start = start 
        self.duration = duration 

    def getProject(self):
        return self.project 

    def getSubproject(self):
        return self.subproject

    def getDay(self):
        return self.day

    def getStart(self):
        return self.start 

    def getDuration(self):
        return self.duration 

