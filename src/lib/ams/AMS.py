
import os.path
import json 

from .actions import * 

class AMS(object):

    ACTIONS = [
        AMSLineCount,
        AMSOrgModeDoneCount,
        AMSOrgModeSectionCount,
        AMSDirectorySize
    ]

    def __init__(self, dbpath):
        self.dbpath = dbpath

    def measure(self, project, subproject):
        """
        Returns list of measurements or throws ManualInputRequiredException
        """
        res = [] 
        spdir = "%s/%s/%s" % (dbpath, project.getName(), subproject.getName())
        if os.path.exists("%s/measure.json" % spdir):
            f = open("%s/measure.json" % spdir, r)
            cfg = json.loads(f.read())
            f.close()
            ms = cfg["measurings"]
            for measurement in ms:
                for action in self.ACTIONS:
                    if cfg["action"] == action.name:
                        action_obj = action(measurement)
                        res.append(action_obj.measure())
                        break
            return res


    def append(self, project, subproject, measurements):
        """
        Adds measurement results into database for specified project and subproject
        """
