
import datetime

class ScheduleCondition(object):
    
    def __init__(self, project_name, subproject_name, description, allowed_days=[1,2,3,4,5,6,7], min_start_by_day=[0,0,0,0,0,0,0], max_start_by_day=[23,23,23,23,23,23,23], min_duration=0, max_duration=23, allowed_dates=list(range(1, 32))):
        self.description = description
        self.project_name = project_name 
        self.subproject_name = subproject_name 
        self.allowed_days = allowed_days
        self.min_start_by_day = min_start_by_day
        self.max_start_by_day = max_start_by_day
        self.min_duration = min_duration
        self.max_duration = max_duration
        self.allowed_dates = allowed_dates

    def getDescription(self):
        return self.description

    def check(self, date_of_creation, entry):
        if self.project_name == entry.getProject().getName() and self.subproject_name == entry.getSubproject().getName():
            if not entry.getDay() in self.allowed_days:
                return False 
            if not (self.min_start_by_day[entry.getDay()] <= entry.getStart() and entry.getStart() <= self.max_start_by_day[entry.getDay()] ):
                return False

            if not (self.min_duration <= entry.getDuration() and entry.getDuration() <= self.max_duration ):
                return False
            wd = date_of_creation.weekday()
            monday = date_of_creation - (datetime.timedelta(days=wd-1))
            if not (monday + datetime.timedelta(days=entry.getDay() - 1)).day in self.allowed_dates:
                return False 
            return True
        return True

    def toDict(self):
        return {
            "description": self.description,
            "project_name": self.project_name,
            "subproject_name": self.subproject_name,
            "allowed_days": self.allowed_days,
            "min_start_by_day": self.min_start_by_day,
            "max_start_by_day": self.max_start_by_day,
            "min_duration": self.min_duration,
            "max_duration": self.max_duration,
            "allowed_dates": self.allowed_dates
        }
    def fromDict(d):
        return ScheduleCondition(**d)
