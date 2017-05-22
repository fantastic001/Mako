
from src.desktop import * 

db = MakoDesktopDatabase("/home/stefan/db/")

projects = db.downloadProjects()

for p in projects:
    print("Project: " + p.getName())
    for sp in p.getSubprojects():
        print("\tSubproject: " + sp.getName())
        for t in sp.getAllTasks():
            print("\t\t| %s \t\t %d \t %d" % (t.getText(), t.getExpectedTime(), t.getSpentTime()))
