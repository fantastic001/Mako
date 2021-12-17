
class Configuration():
    def open(self) -> dict:
        raise NotImplemented()

    def save(self, params: dict):
        raise NotImplemented()
    
    def getProperty(self, prop: str, defaultValue):
        params = self.open()
        return params.get(prop, defaultValue)
    
    def setProperty(self, prop: str, value):
        params = self.open()
        params[prop] = value
        self.save(params)
