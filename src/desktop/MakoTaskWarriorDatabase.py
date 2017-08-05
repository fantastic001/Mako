
from ..lib.database import * 
from ..lib.schedule import * 

import os

import datetime

class MakoTaskWarriorDatabase(MakoDatabase):
    """
    Params to constructor:

    path: path to taskwarrior database 
    """
    
    def init(self):
        pass

    def validate(self):
        return True

    def parseLine(self, line):
        line = line[1:-1]
        kv = []
        curr = ""
        state = 0
        for c in line:
            if c == " " and state == 0:
                kv.append(curr)
                curr = ""
            elif c in "'\"" and state == 0:
                state = 1
                curr += c
            elif c in "'\"" and state == 1:
                state = 0
                curr += c
            elif c == " " and state == 1:
                curr = curr + c 
            elif c != " " and state == 0:
                curr += c
            else:
                curr += c
        if curr != "":
            kv.append(curr)
        d = {}
        for k in kv:
            if not ":" in k:
                continue
            key = k.split(":")[0]
            val = k.split(":")[1][1:-1] # we remove quotes
            d[key] = val
        return d

    def getProject(self, projects, d):
        pname = d.get("project", "unknown")
        for project in projects:
            if pname == project.getName():
                return project
        projects.append(ScheduleProject(pname, (255,255,255), (0,0,0)))
        return projects[-1]

    def getSubproject(self, project, d):
        spname = d.get("tags", "unknown").split(",")[0]
        for subproject in project.getSubprojects():
            if subproject.getName() == spname:
                return subproject
        project.addSubproject(ScheduleSubproject(spname))
        return project.getSubprojects()[-1]
    
    def getTask(self, d):
        due = None
        if "due" in d.keys():
            due = datetime.datetime(1970,1,1) + datetime.timedelta(seconds=int(d["due"]))
        return Task(d.get("description", ""), 1, due=due, done=(d.get("status", "pending")=="completed"))
    
    def uploadProjects(self, projects):
        f = open("%s/pending.data" % self.getParams()["path"], "w")
        for project in projects:
            for subproject in project.getSubprojects():
                for task in subproject.getAllTasks():
                    status = "pending"
                    if task.isDone():
                        status = "completed"
                    due = ""
                    if task.getDueDate() != None:
                        dt = (task.getDueDate() - datetime.datetime(1970, 1, 1)).total_seconds()
                        due = str(int(dt))
                    description = task.getText()
                    pname = project.getName()
                    tags = subproject.getName()
                    C = ""
                    if due != "":
                        C = "due:\"%s\"" % due
                    f.write('[description:"%s" project:"%s" %s status:"%s" tags:"%s"]\n' % (description,pname,C, status, tags))
        f.close()

    def uploadMeasurementActions(self, actions):
        pass

    def uploadMeasurementData(self, action_id, data):
        """
        data is list of tuples sorted by date from odler to newer

        first element in tuple is date 
        second element is value 
        """
        pass

    def uploadData(self, data):
        """
        Data is list of tuples where first element is name and second concrete data 
        """
        pass

    def uploadSchedules(self, schedules):
        """
        schedules: list of Schedule objects:

        """
        pass

    def uploadReports(self, reports):
        pass

    def uploadDefaultConditions(self, conditions):
        pass

    def uploadTables(self, tables):
        pass
    
    def downloadProjects(self):
        projects = [] 
        f = open("%s/pending.data" % self.getParams()["path"])
        for line in f:
            d = self.parseLine(line)
            if d.get("description", "") != "":
                project = self.getProject(projects, d)
                subproject = self.getSubproject(project, d)
                subproject.addTask(self.getTask(d))
        f.close()
        return projects

    def downloadMeasurementActions(self):
        return []

    def downloadMeasurementData(self, action_id):
        """
        data is list of tuples sorted by date from odler to newer

        first element in tuple is date 
        second element is value 
        """
        return []

    def downloadData(self):
        """
        Returns list of tuples where first element is name and second is data 
        """
        pass

    def downloadSchedules(self):
        """
        Returns list of Schedule object
        """
        return []

    def downloadReports(self):
        return []

    def downloadDefaultConditions(self):
        """
        Returns list of conditions for schedule
        """
        return []

    def downloadTables(self):
        return []

