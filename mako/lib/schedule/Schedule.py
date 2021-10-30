
import datetime 

from .ScheduleProject import * 
from .ScheduleSubproject import * 
from .ScheduleEntry import * 
from .ScheduleCondition import * 
import json

class Schedule(object):

    def __init__(self, date):
        self.date = date 
        self.entries = [] 
        self.conditions = [] 
    
    def __hash__(self):
        return hash(json.dumps(self.toDict(), sort_keys=True))

    def __eq__(self, other):
        return json.dumps(self.toDict(), sort_keys=True) == json.dumps(other.toDict(), sort_keys=True)

    def addCondition(self, cond):
        self.conditions.append(cond)

    def getConditions(self):
        return self.conditions

    def check(self):
        """
        Returns: list of pairs where first element is entry and second is condition which is unsatisfied.
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

    def removeEntry(self, day, start, duration):
        """
        Removes all entries which are scheduled for the specified day between start and start+duration 

        If entry starts at exactly start, it will be removed also but if it starts at start+duration, it won't be removed.
        """
        result = []
        for i in range(len(self.entries)):
            entry = ScheduleEntry.fromDict(self.entries[i].toDict())
            if day == self.entries[i].getDay():
                if (start > self.entries[i].getStart() or self.entries[i].getStart() >= start+duration) and (self.entries[i].getStart() > start or start+duration > self.entries[i].getStart() + self.entries[i].getDuration()):
                    result.append(entry)
                else:
                    if duration < entry.getDuration():
                        # now we have to add rest back 
                        if entry.getStart() == start:
                            result.append(ScheduleEntry(entry.getProject(), entry.getSubproject(), entry.getDay(), entry.getStart() + duration, entry.getDuration() - duration))
                        elif entry.getStart() < start and start + duration < entry.getStart() + entry.getDuration():
                            result.append(ScheduleEntry(entry.getProject(), entry.getSubproject(), entry.getDay(), entry.getStart(), start - entry.getStart()))
                            result.append(ScheduleEntry(entry.getProject(), entry.getSubproject(), entry.getDay(), start + duration, entry.getStart() + entry.getDuration() - start - 1))
                        else:
                            result.append(ScheduleEntry(entry.getProject(), entry.getSubproject(), entry.getDay(), entry.getStart(), entry.getDuration() - duration))
            else:
                result.append(entry)
        self.entries = result
    def tasksToday(self, projects, day, added=[]):
        """
        Returns list of tasks scheduled for given day based on this schedule.

        Args:
            projects: list of ScheduleProject objects to select tasks from 
            day: specification of the day as int (1 for Monday, 7 for Sunday)
        Returns: list of tuples (p,sp,t) where p is ScheduleProject object, sp is ScheduleSubproject object and t is Task object
        """
        entries = [entry for entry in self.entries if entry.getDay() == day]
        if entries == []:
            return []
        head, *tail = entries 
        tasks = [(p, sp, i, task) for p in projects 
            for sp in p.getSubprojects() 
            for i, task in enumerate(sp.getAllTasks()) 
            if not task.isDone() and not (p,sp,i,task) in added
        ]
        tasks = sorted(tasks, key=lambda x: x[3].getDueDate())
        l = [(p, sp, i, t) for p,sp,i,t in tasks 
            if head.getProject().getName() == p.getName() and head.getSubproject().getName() == sp.getName()
        ]
        if l == []:
            return Schedule.fromDict(dict(
                self.toDict(), entries=[e.toDict() for e in tail]
            )).tasksToday(projects, day, added)
        first, *rest = l
        fp, fsp, _, ft = first
        if head.getDuration() > ft.getExpectedTime():
            return [(fp, fsp, ft)] + Schedule.fromDict(dict(
                self.toDict(), 
                entries=[dict(head.toDict(), duration=head.getDuration() - ft.getExpectedTime())] + [
                    e.toDict() for e in tail
                ]
            )).tasksToday(projects, day, [first] + added)
        elif head.getDuration() == ft.getExpectedTime():
            return [(fp, fsp, ft)] + Schedule.fromDict(dict(
                self.toDict(), 
                entries=[e.toDict() for e in tail]
            )).tasksToday(projects, day, [first] + added)
        else:
            return [(fp, fsp, ft)] + Schedule.fromDict(dict(
                self.toDict(), entries=[e.toDict() for e in tail]
            )).tasksToday(projects, day, [first] + added)

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
