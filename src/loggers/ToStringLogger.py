from .BaseLogger import * 
import colorama

class ToStringLogger(BaseLogger):

    def __init__(self):
        self.s  = ""

    def short_title(self, task):
        if len(task.getText()) > 30:
            return task.getText()[:30] + "..."
        return task.getText()
    
    def print(self, text):
        self.s += text + "\n"

    def task(self, task, identifier=None):
        text = self.short_title(task)
        color = "[ ]"
        if task.isDone():
            color = "[X]"
        if identifier is None:
            self.s += "%s\t\t| %s | %s | %s %d \t %d%s\n" % (color, text, str(task.getDueDate()), " " * (40 - len(text)), task.getExpectedTime(), task.getSpentTime(), "")
        else:
            self.s += "%d %s\t\t| %s | %s | %s %d \t %d%s\n" % (identifier, color, text, str(task.getDueDate()), " " * (40 - len(text)), task.getExpectedTime(), task.getSpentTime(), "")

    def title(self, title):
        self.s += "%s\n" % title

    def table(self, table, has_header=True):
        """
        table: list of lists
        """
        column_size = 10
        if len(table) == 0:
            return 
        l = len(table[0])
        for row in table:
            if l != len(row):
                self.s += "Table not alligned"
                return 
        i = 0
        for row in table:
            s = "|"
            for column in row:
                if len(column) > column_size:
                    column = column[:column_size]
                s += " %s |" % (column + " "* (column_size - len(column)))
            self.s += s+ "\n"
            i = i + 1
            if has_header and i == 1:
                self.s += "-" * (1 + (3 + column_size) * len(row)) + "\n"

    def schedule(self, schedule):
        e = schedule.getEntries()
        table = [["Time", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]]
        for t in range(24):
            l = [str(t) + ":00"] 
            for day in range(1, 8):
                # now we search for entry, if exists 
                entry = None 
                for ee in e:
                    if ee.getDay() == day and ee.getStart() <= t and t < ee.getStart() + ee.getDuration():
                        entry = ee 
                if entry == None:
                    l.append("")
                else:
                    l.append(entry.getProject().getName()[:3] + " - " + entry.getSubproject().getName())
            table.append(l)
        self.table(table)

    def clear(self):
        self.s = ""

    def get(self):
        res = self.s.replace("\t", "    ")
        print(res)
        return res
