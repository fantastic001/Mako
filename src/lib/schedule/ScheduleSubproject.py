
import datetime

class ScheduleSubproject(object):

    def __init__(self, name):
        self.name = name 
        self.tasks = [] 

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
