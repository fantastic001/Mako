
class Table(object):
    
    def __init__(self, name, fields):
        self.name = name 
        self.fields = fields
        self.entries = []

    def getName(self):
        return self.name

    def getFields(self):
        return self.fields

    def getEntries(self):
        return self.entries 

    def addEntry(self, e):
        self.entries.append(e)

    def removeEntry(self, k):
        if k > 0 and k <= len(self.entries):
            del(self.entries[k-1])

    def updateEntry(self, k, e):
        if k > 0 and k <= len(self.entries):
            self.entries[k-1] = e 

    def getEntryCount(self):
        return len(self.entries)

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
