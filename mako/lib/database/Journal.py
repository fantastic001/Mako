
class Journal(object):
    def commit(self, data):
        raise NotImplemented()
    def register(self):
        raise NotImplemented()
    def mark(self):
        raise NotImplemented()
    def getLast(self):
        raise NotImplemented()
    def isMarked(self):
        raise NotImplemented()
    def isRegistered(self):
        raise NotImplemented()