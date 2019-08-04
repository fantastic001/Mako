import json 


class Table(object):
    
    def __init__(self, name, fields):
        """
        Args:
            name: name of the table
            fields: list of strings specifying column names
        """
        self.name = name 
        self.fields = fields
        self.entries = []

    def __hash__(self):
        return hash(json.dumps(self.toDict(), sort_keys=True))

    def __eq__(self, other):
        return json.dumps(self.toDict(), sort_keys=True) == json.dumps(other.toDict(), sort_keys=True)

    def getName(self):
        return self.name

    def getFields(self):
        """
        Gets header of table

        Returns: list of strings representing individual column names
        """
        return self.fields

    def getEntries(self, search=None):
        """
        Gets entries of table with possibly filtered results.

        Args:
            search: if None, gets all entries, if string, gets entries where at least one column has search pattern in its string.
        Returns: list of lists, every list has elements for every column sorted as fields
        """
        if search == None:
            return self.entries 
        else:
            res = [] 
            for e in self.entries:
                found = False 
                for f in e:
                    if search in f:
                        res.append(e)
            return res

    def addEntry(self, e):
        """
        Adds entry to table

        Args:
            e: list of values for every column. Size of e has to be equal to size of fields supplied in constructor.
        """
        self.entries.append(e)

    def removeEntry(self, k):
        """
        Deletes kth entry in table where k = 1...N where N is number of entries. 
        
        Args:
            k: index of row to delete. Ordering starts from 1.
        """
        if k > 0 and k <= len(self.entries):
            del(self.entries[k-1])

    def updateEntry(self, k, e):
        """
        Updates kth entry with new data. 

        Please see addEntry and removeEntry
        """
        if k > 0 and k <= len(self.entries):
            self.entries[k-1] = e 

    def getEntryCount(self, search=None):
        return len(self.getEntries(search))

    def toDict(self):
        d = {}
        d["name"] = self.name 
        d["fields"] = self.fields 
        d["entries"] = [] 
        for e in self.entries:
            d["entries"].append(e)
        return d 

    def fromDict(d):
        table = Table(d["name"], d["fields"])
        for e in d["entries"]:
            table.addEntry(e)
        return table

    def __str__(self):
        s = "\n"
        column_size = 60 // len(self.getFields())
        header = ["No"] + self.getFields()
        s += "|"
        for i in range(len(header)):
            column = header[i]
            if i == 0:
                k = 5
            else:
                k = column_size
            if len(column) > k:
                column = column[:k]
            s += " %s |" % (column + " "* (k - len(column)))
        s += "\n"
        s += "-" * (9 + (3 + column_size) * (len(header) - 1))
        s += "\n"
        i = 1
        for row in self.getEntries():
            s += "| %s%s |" % (str(i), " " * (5-len(str(i))))
            for column in row:
                if len(column) > column_size:
                    column = column[:column_size]
                s += " %s |" % (column + " "* (column_size - len(column)))
            i = i + 1
            s += "\n"
        return s 
