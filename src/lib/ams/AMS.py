
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

    def measure(self, project, subproject, ms):
        """
        Returns list of measurements or throws ManualInputRequiredException

        ms: list of measuring dictionary with the following fields
            
            action: action (method) to perform measurement
            ... every other field is specific to the action 
        """
        res = [] 
        for measurement in ms:
            for action in self.ACTIONS:
                if measurement["action"] == action.name:
                    action_obj = action(measurement["id"], measurement.get("description", ""), measurement)
                    res.append(action_obj.measure())
                    break
        return res



