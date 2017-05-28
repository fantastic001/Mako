
from src.desktop import * 

import colorama

def short_title(task):
    if len(task.getText()) > 30:
        return task.getText()[:30] + "..."
    return task.getText()

db = MakoDesktopDatabase("/home/stefan/db/")
db2 = MakoDesktopDatabase("/home/stefan/db2/")

projects = db.downloadProjects()
db2.uploadProjects(projects)

for p in projects:
    print("Project: " + p.getName())
    for sp in p.getSubprojects():
        print("\tSubproject: " + sp.getName())
        for t in sp.getAllTasks():
            text = short_title(t)
            color = colorama.Fore.RED
            if t.isDone():
                color = colorama.Fore.GREEN
            print("%s\t\t| %s | %s | %s %d \t %d%s" % (color, text, str(t.getDueDate()), " " * (40 - len(text)), t.getExpectedTime(), t.getSpentTime(), colorama.Style.RESET_ALL))


print("_" * 50)
print("Metrics:")
metrics = db.downloadMeasurementActions()
db2.uploadMeasurementActions(metrics)
for metric in metrics:
    print("%s\t%s" % (metric.getIdentifier(), metric.getDescription()))
    data = db.downloadMeasurementData(metric.getIdentifier())
    print("\tLast: %f on %s" % (data[-1][1], str(data[-1][0])))
    db2.uploadMeasurementData(metric.getIdentifier(), data)

print("_" * 50)
print("Schedules:")
schedules = db.downloadSchedules()
db2.uploadSchedules(schedules)
for schedule in schedules:
    d, p, e = schedule
    print("Schedule created %s" % str(d))

print("_" * 50)
print("Reports")
reports = db.downloadReports()
db2.uploadReports(reports)
for r in reports:
    print(r.getName() + " created " + str(r.getDate()))
