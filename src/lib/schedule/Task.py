
import datetime

class Task(object):
    
    def __init__(self, text, expected, spent=0, done=False, due=None):
        """
        due: Due date as datetime.date object
        """
        self.text = text 
        self.expected = expected 
        self.spent = spent 
        self.done = done
        if type(due) == datetime.datetime:
            self.due = due.date()
        else:
            self.due = due

    def getText(self):
        return self.text 

    def getExpectedTime(self):
        return self.expected 

    def getSpentTime(self):
        return self.spent 

    def isDone(self):
        return self.done 

    def increaseSpentTime(self, dt):
        self.spent = self.spent + dt

    def getDueDate(self):
        return self.due

    def setDone(self):
        self.done = True

    def toDict(self):
        d = {}
        d["text"] = self.text
        d["expected"] = self.expected
        d["spent"] = self.spent
        d["done"] = self.done
        if self.due != None:
            d["due"] = datetime.datetime.strftime(self.due, "%Y-%m-%d")
        return d 

    def fromDict(d):
        return Task(d["text"], int(d["expected"]), int(d["spent"]), bool(d["done"]), datetime.datetime.strptime(d.get("due", None), "%Y-%m-%d"))
