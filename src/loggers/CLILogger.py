from .BaseLogger import * 
import colorama

class CLILogger(BaseLogger):

    def short_title(self, task):
        if len(task.getText()) > 30:
            return task.getText()[:30] + "..."
        return task.getText()
    
    def print(self, text):
        print(text)

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
