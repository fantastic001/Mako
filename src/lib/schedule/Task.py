
class Task(object):
    
    def __init__(self, text, expected, spent=0, done=False, due=None):
        """
        due: Due date as datetime.date object
        """
        self.text = text 
        self.expected = expected 
        self.spent = spent 
        self.done = done
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
