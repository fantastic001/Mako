
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
