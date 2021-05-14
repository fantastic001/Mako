
from . import MakoDatabase, Journal

class JournaledDatabase(MakoDatabase):
    def init(self):
        """
        Implementation of database has to implement. 

        Initialize database (assume it does not exist).
        """
        self.journal = self.getParams()["journal"]
        self.db = self.getParams()["db"]
        if not self.journal.isRegistered():
            self.journal.register()
            self.journal.mark()
            return 
        if not self.journal.isMarked():
            self.db.fromDict(self.journal.getLast())

    def validate(self):
        return False

    def uploadProjects(self, projects):
        """
        Implementation of database has to implement. 

        Perform writing of list of projects to database. 

        Args:
            projects: list of ScheduleProject objects.
        """
        self.journal.commit(self.toDict())

    def uploadMeasurementActions(self, actions):
        """
        Implementation of database has to implement. 

        Writes measurement actions to database. 

        Args:
            actioins: list of BaseAction or derived objects.
        """
        self.journal.commit(self.toDict())
        

    def uploadMeasurementData(self, action_id, data):
        """
        Implementation of database has to implement. 

        data is list of tuples sorted by date from odler to newer

        first element in tuple is date 
        second element is value 

        Args:
            action_id: action id for which data is uploaded (see name field for every action implementation)
            data: data structured as explained above
        """
        self.journal.commit(self.toDict())


    def uploadData(self, data):
        """
        Implementation of database has to implement.

        Data is list of tuples where first element is name and second concrete data 

        Args:
            data: data structured as explained above
        """
        self.journal.commit(self.toDict())

    def uploadSchedules(self, schedules):
        """
        Implementation of database has to implement.

        Args:
            schedules: list of Schedule objects:

        """
        self.journal.commit(self.toDict())
        

    def uploadReports(self, reports):
        """
        Implementation of database has to implement.

        Args:
            reports: list of Report objects

        """
        self.journal.commit(self.toDict())
        

    def uploadDefaultConditions(self, conditions):
        """
        Implementation of database has to implement.

        default conditions are schedule coonditions applied for every schedule by default and they are added by user. 

        Args:
            conditions: list of ScheduleCondition objects

        """
        self.journal.commit(self.toDict())
        

    def uploadTables(self, tables):
        """
        Implementation of database has to implement.

        Args:
            tables: list of Table objects

        """
        self.journal.commit(self.toDict())
        

    def downloadProjects(self):
        """
        Implementation of database has to implement.

        Returns: list of ScheduleProject objects

        """
        return self.db.downloadProjects()

    def downloadMeasurementActions(self):
        """
        Implementation of database has to implement.

        Returns: list of BaseAction objects
        """
        return self.db.downloadMeasurementActions()

    def downloadMeasurementData(self, action_id):
        """
        Implementation of database has to implement.
        data is list of tuples sorted by date from odler to newer

        first element in tuple is date 
        second element is value 
        Args:
            action_id: action name for which data is requested.
        Returns: data

        """
        return self.db.downloadMeasurementData(action_id)

    def downloadData(self):
        """
        Implementation of database has to implement.

        Returns: list of tuples where first element is name and second is data 
        """
        return self.db.downloadData()

    def downloadSchedules(self):
        """
        Implementation of database has to implement.

        Returns: list of Schedule object
        """
        return self.db.downloadSchedules()

    def downloadReports(self):
        """
        Implementation of database has to implement.

        Returns: list of Report objects
        """
        return self.db.downloadReports()

    def downloadDefaultConditions(self):
        """
        Implementation of database has to implement.

        Returns: list of ScheduleCondition objects
        """
        return self.db.downloadDefaultConditions()

    def downloadTables(self):
        """
        Implementation of database has to implement.

        Returns: list of Table objects
        """
        return self.db.downloadTables()