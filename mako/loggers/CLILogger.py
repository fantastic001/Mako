from .BaseLogger import * 
import colorama

import json

class CLILogger(BaseLogger):

    def __init__(self, debug=False) -> None:
        super().__init__()
        self._debug = debug

    def short_title(self, task):
        if len(task.getText()) > 30:
            return task.getText()[:30] + "..."
        return task.getText()
    
    def print(self, text=""):
        print(text)

    def green(self, text):
        print(colorama.Fore.GREEN + text + colorama.Style.RESET_ALL)
    def red(self, text):
        print(colorama.Fore.RED + text + colorama.Style.RESET_ALL)

    def task(self, task, identifier=None):
        text = self.short_title(task)
        color = colorama.Fore.RED
        if task.isDone():
            color = colorama.Fore.GREEN
        if identifier is None:
            print("%s\t\t| %s | %s | %s %d \t %d%s" % (color, text, str(task.getDueDate()), " " * (40 - len(text)), task.getExpectedTime(), task.getSpentTime(), colorama.Style.RESET_ALL))
        else:
            print("%d %s\t\t| %s | %s | %s %d \t %d%s" % (identifier, color, text, str(task.getDueDate()), " " * (40 - len(text)), task.getExpectedTime(), task.getSpentTime(), colorama.Style.RESET_ALL))

    def title(self, title):
        print("%s:" % title)
        print("_________________")

    def table(self, table, has_header=True, column_size=10):
        """
        table: list of lists
        """
        if len(table) == 0:
            return 
        l = len(table[0])
        for row in table:
            if l != len(row):
                print("Table not alligned")
                return 
        i = 0
        for row in table:
            s = "|"
            for column in row:
                if len(column) > column_size:
                    column = column[:column_size]
                s += " %s |" % (column + " "* (column_size - len(column)))
            print(s)
            i = i + 1
            if has_header and i == 1:
                print("-" * (1 + (3 + column_size) * len(row)))

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
    
    def diff(self, diff):
        """
        diff: diff object returned from Database.diff method
        """
        res = diff 
        self.title("Projects")
        for x in res["projects"]["added"]:
            self.green("+ %s" % x)
        for x in res["projects"]["removed"]:
            self.red("- %s" % x)

        self.title("Subprojects")
        for x, y in res["subprojects"]["added"]:
            self.green("+ %s" % y)
        for x, y in res["subprojects"]["removed"]:
            self.red("- %s" % y)

        self.title("Tasks")
        for x,y,z in res["tasks"]["added"]:
            self.green("+ %s %s %s" % (x,y,json.dumps(z.toDict())))
        for x,y,z in res["tasks"]["removed"]:
            self.red("- %s %s %s" % (x,y,json.dumps(z.toDict())))

        self.title("Schedules")
        for x in res["schedules"]["added"]:
            self.green("+ %s" % json.dumps(x.toDiict()))
        for x in res["schedules"]["removed"]:
            self.red("- %s" % json.dumps(x.toDiict()))

        self.title("Tables")
        for x in res["tables"]["added"]:
            self.green("+ %s" % json.dumps(x.toDiict()))
        for x in res["tables"]["removed"]:
            self.red("- %s" % json.dumps(x.toDiict()))

        self.title("Reports")
        for x in res["reports"]["added"]:
            self.green("+ %s" % json.dumps(x.toDict()))
        for x in res["reports"]["removed"]:
            self.red("- %s" % json.dumps(x.toDict()))

        self.title("Metrics")
        for x in res["metrics"]["added"]:
            self.green("+ %s" % json.dumps(x.toDict()))
        for x in res["metrics"]["removed"]:
            self.red("- %s" % json.dumps(x.toDict()))

        self.title("Conditions")
        for x in res["conditions"]["added"]:
            self.green("+ %s" % json.dumps(x.toDict()))
        for x in res["conditions"]["removed"]:
            self.reed("- %s" % json.dumps(x.toDict()))

        self.title("Data")
        for x in res["data"]["added"]:
            self.green("+ %s" % json.dumps(x.toDict()))
        for x in res["data"]["removed"]:
            self.red("- %s" % json.dumps(x.toDict()))

        self.title("Measurements")
        for x,y in res["measurements"]["added"]:
            self.green("+ %s %s %f" % (x.GetIdentifier(), str(y[0]), [1]))
        for x in res["measurements"]["removed"]:
            self.red("- %s %s %f" % (x.GetIdentifier(), str(y[0]), [1]))

    def debug(self, text):
        if self._debug:
            print("DEBUG: %s" % text)