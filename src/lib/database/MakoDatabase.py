
class MakoDatabase(object):

    def uploadProjects(self, projects):
        pass

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
        schedules: list of tuples where:

        1. element: date of creation (or None if db does not provide it)
        2. element: list of all projects 
        3. element: list of schedule entries
        """
        pass

    def uploadReports(self, reports):
        pass


    def downloadProjects(self):
        pass

    def downloadMeasurementActions(self):
        pass

    def downloadMeasurementData(self, action_id):
        """
        data is list of tuples sorted by date from odler to newer

        first element in tuple is date 
        second element is value 
        """
        pass

    def downloadData(self):
        """
        Returns list of tuples where first element is name and second is data 
        """
        pass

    def downloadSchedules(self):
        """
        Returns list of tuples where:

        1. element: date of creation (or None if db does not provide it)
        2. element: list of all projects 
        3. element: list of schedule entries
        """
        pass

    def downloadReports(self):
        pass
