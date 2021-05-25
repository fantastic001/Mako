
from mako.lib.StatusListener import * 

class CLIStatusListener(StatusListener):
    def onError(self, msg):
        print("ERROR: %s" % msg)
    def onWarning(self, msg):
        print("WARNING: %s" % msg)
    def onSuccess(self, msg):
        print("INFO: %s" % msg)
    def onDatabaseUpdate(self, db):
        pass
    def onNewTask(self, project, subproject, task):
        pass
    def onScheduleUpdate(self, schedule):
        pass