

class ScheduleReader(object):
    """
    How to use:

    reader = ScheduleReader()
    reader.open(param1=val1, param2=val2, ...)
    reader.read()
    reader.close()

    schedule = reader.getSchedule()
    """
    
    def open(self, **kw):
        """
        This method should implement opening file or stream.

        kw: parameters to the reader
        """
        pass


    def close(self):
        """
        Implements closing.
        """
        pass

    def read(self):
        """
        Should return Schedule object
        """
