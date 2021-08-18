
class BaseLogger(object):
    
    def print(self, text=""):
        pass

    def task(self, task, identifier=None):
        pass

    def title(self, title):
        pass

    def table(self, table, has_header=True, column_size=10):
        pass

    def schedule(self, schedule):
        pass

    def diff(self, diff):
        """
        diff: diff object returned from Database.diff method
        """
        pass
    def debug(self, text):
        pass
