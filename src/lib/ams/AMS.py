
import os.path
import json 
import datetime

from .actions import * 

class AMS(object):

    ACTIONS = [
        AMSLineCountAction,
        AMSOrgModeDoneCountAction,
        AMSOrgModeSectionCountAction,
        AMSTableEntryCountAction,
        AMSDirectorySizeAction
    ]

    def measure(self, project, subproject, tables, ms):
        """
        Returns list of measurements or throws ManualInputRequiredException

        to thi method, it must be provided tables of the database 

        ms: list of measuring dictionary with the following fields
            
            action: action (method) to perform measurement
            id: id of specific action in database 
            description: description of concrete action
            ... every other field is specific to the action 
        """
        res = [] 
        for measurement in ms:
                res.append(self.getAction(measurement).measure(tables))
        return res

    def getAction(self, measurement):
        """
        Returns concrete action specified by ms dictionary

        see documentation for measure(...) for morre info about data in dictioary 
        """
        for action in self.ACTIONS:
            if measurement["action"] == action.name:
                return action(measurement["id"], measurement.get("description", ""), measurement)




