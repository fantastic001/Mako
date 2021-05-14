
import datetime
import json

class ScheduleCondition(object):
    
    def __init__(self, project_name, subproject_name, description, allowed_days=[1,2,3,4,5,6,7], min_start_by_day=[0,0,0,0,0,0,0], max_start_by_day=[23,23,23,23,23,23,23], min_duration=0, max_duration=23, allowed_dates=list(range(1, 32))):
        """
        Construct constraint on schedule

        Args:
           project_name: name of the project. Only entries with that project name are considered for check. 
           subproject_name: name of subproject, only entries with this subproject are coonsidered in check 
           description: Description of condition as a string
           allowed_days=[1,2,3,4,5,6,7]: days when entries with given project name and subproject name can be allowed in schedule
           min_start_by_day=[0,0,0,0,0,0,0]: list of 7 integers indicating minimal time for every day in a week when entries with specified project name and subproject name can occur
           max_start_by_day=[23,23,23,23,23,23,23]: same as for min_start_by_day but upper bound
           min_duration=0: minimal duration per entry (block size in schedule)
           max_duration=23: maximal duration per entry (block size in schedule)
           allowed_dates=list(range(1, 32): allowed dates when this entry can be in schedule.
        """
        self.description = description
        self.project_name = project_name 
        self.subproject_name = subproject_name 
        self.allowed_days = allowed_days
        self.min_start_by_day = min_start_by_day
        self.max_start_by_day = max_start_by_day
        self.min_duration = min_duration
        self.max_duration = max_duration
        self.allowed_dates = allowed_dates
    
    def __hash__(self):
        return hash(json.dumps(self.toDict(), sort_keys=True))

    def __eq__(self, other):
        return json.dumps(self.toDict(), sort_keys=True) == json.dumps(other.toDict(), sort_keys=True)

    def getDescription(self):
        return self.description

    def check(self, date_of_creation, entry):
        """
        Check if given entry satisfied constraint.

        Args:
            date_of_creation: date or datetime object when schedule containing given entry is created.
            entry: ScheduleEntry object to check
        Returns: True if condition is satisfied, Fallse otherwise.
        """
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
