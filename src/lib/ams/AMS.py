
import os.path
import json 
import datetime

from .actions import * 

class AMS(object):

    ACTIONS = [
        AMSLineCountAction,
        AMSOrgModeDoneCountAction,
        AMSOrgModeSectionCountAction,
        AMSDirectorySizeAction
    ]

    def __init__(self, dbpath):
        self.dbpath = dbpath

    def measure(self, project, subproject):
        """
        Returns list of measurements or throws ManualInputRequiredException
        """
        res = [] 
        spdir = "%s/%s/%s" % (self.dbpath, project.getName(), subproject.getName())
        if os.path.exists("%s/measure.json" % spdir):
            f = open("%s/measure.json" % spdir, "r")
            cfg = json.loads(f.read())
            f.close()
            ms = cfg["measurings"]
            for measurement in ms:
                for action in self.ACTIONS:
                    if measurement["action"] == action.name:
                        action_obj = action(measurement)
                        res.append(action_obj.measure())
                        break
            return res


    def append(self, project, subproject, measurements):
        """
        Adds measurement results into database for specified project and subproject
        """
        today = datetime.date.today().strftime("%d.%m.%Y.")
        res = [today]
        for m in measurements:
            res.append(str(m))
        nline = ",".join(res)
        lines = []
        fname = "%s/%s/%s/progress.csv" % (self.dbpath, project.getName(), subproject.getName())
        f = open(fname, "r")
        for line in f:
            lines.append(line)
        f.close()
        if today == lines[-1].split(",")[0]: 
            return 
        lines.append(nline)
        f = open(fname, "w")
        for line in lines:
            f.write(line)
        f.close()


