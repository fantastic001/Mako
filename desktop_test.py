
from src.desktop import * 

import colorama

def short_title(task):
    if len(task.getText()) > 30:
        return task.getText()[:30] + "..."
    return task.getText()

db = MakoDesktopDatabase("/home/stefan/db/")

projects = db.downloadProjects()

for p in projects:
    print("Project: " + p.getName())
    for sp in p.getSubprojects():
        print("\tSubproject: " + sp.getName())
        for t in sp.getAllTasks():
            text = short_title(t)
            color = colorama.Fore.RED
            if t.isDone():
                color = colorama.Fore.GREEN
            print("%s\t\t| %s %s %d \t %d%s" % (color, text, " " * (40 - len(text)), t.getExpectedTime(), t.getSpentTime(), colorama.Style.RESET_ALL))


print("_" * 50)
print("Metrics:")
metrics = db.downloadMeasurementActions()
for metric in metrics:
    print("%s\t%s" % (metric.getIdentifier(), metric.getDescription()))
    last = db.downloadMeasurementData(metric.getIdentifier())[-1]
    print("\tLast: %f on %s" % (last[1], str(last[0])))

print("_" * 50)
print("Schedules:")
schedules = db.downloadSchedules()
for schedule in schedules:
    d, p, e = schedule
    print("Schedule created %s" % str(d))

print("_" * 50)
print("Reports")
for r in db.downloadReports():
    print(r.getName() + " created " + str(r.getDate()))
