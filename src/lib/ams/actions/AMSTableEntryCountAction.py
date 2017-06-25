
import os 
from .AMSBaseAction import * 

class AMSTableEntryCountAction(AMSBaseAction):
    """
    Counts entries in a table 

    Parameters:
    table_name: name of a table
    filter: filter to search for
    
    """

    name = "table.entry.count"
    description = ""
    identifier = "" # identifies specific action in database

    def measure(self, tables):
        table_name = self.getConfig().get("table_name", "")
        for table in tables:
            if table.getName() == table_name:
                if self.getConfig().get("filter", "") != "":
                    return table.getEntryCount(self.getConfig().get("filter", ""))
                return table.getEntryCount()
        return 0 
