
from .MakoDatabase import * 

class MakoMemoryDatabase(MakoDatabase):
    """
    Parameters to constructor

    frequency: number of uploads after which data is exported into database for permament saving 
    db: database responsible to save all data
    """

    def init(self):
        self.freq = self.getParams().get("frequency",  10)
        self.db = self.getParams()["db"]
        
        self.count = 0 

        self.projects = []
        self.actions = []
        self.measurements = {}
        self.schedules = []
        self.reports = []
        self.tables = []
        self.data = []
        self.conditions = []
        if not self.db.validate():
            self.db.init()
        self.db.export(self)



    def validate(self):
        return False

    def handleExports(self):
        self.count += 1 
        if self.count >= self.freq:
            self.count = 0 
            self.export(self.db)

    def uploadProjects(self, projects):
        self.projects = projects
        self.handleExports()

    def uploadMeasurementActions(self, actions):
        self.actions = actions
        self.handleExports()

    def uploadMeasurementData(self, action_id, data):
        """
        data is list of tuples sorted by date from odler to newer

        first element in tuple is date 
        second element is value 
        """
        self.measurements[action_id] = data
        self.handleExports()

    def uploadData(self, data):
        """
        Data is list of tuples where first element is name and second concrete data 
        """
        self.data = data
        self.handleExports()

    def uploadSchedules(self, schedules):
        """
        schedules: list of Schedule objects:

        """
        self.schedules = schedules
        self.handleExports()

    def uploadReports(self, reports):
        self.reports = reports
        self.handleExports()

    def uploadDefaultConditions(self, conditions):
        self.conditions = conditions
        self.handleExports()

    def uploadTables(self, tables):
        self.tables = tables
        self.handleExports()
    
    def downloadProjects(self):
        return self.projects

    def downloadMeasurementActions(self):
        return self.actions 

    def downloadMeasurementData(self, action_id):
        """
        data is list of tuples sorted by date from odler to newer

        first element in tuple is date 
        second element is value 
        """
        return self.measurements[action_id]

    def downloadData(self):
        """
        Returns list of tuples where first element is name and second is data 
        """
        return self.data

    def downloadSchedules(self):
        """
        Returns list of Schedule object
        """
        return self.schedules

    def downloadReports(self):
        return self.reports

    def downloadDefaultConditions(self):
        """
        Returns list of conditions for schedule
        """
        return self.conditions

    def downloadTables(self):
        return self.tables

    def save(self):
        self.export(self.db)
