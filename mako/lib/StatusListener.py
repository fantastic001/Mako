
class StatusListener(object):
    def onError(self, msg):
        pass
    def onWarning(self, msg):
        pass
    def onSuccess(self, msg):
        pass
    def onDatabaseUpdate(self, db):
        pass
    def onNewTask(self, project, subproject, task):
        pass
    def onScheduleUpdate(self, schedule):
        pass