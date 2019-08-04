
import json
import os

class ConfigManager(object):
    
    def __init__(self, path, intime=True):
        """
        Initialize coonfiguration object for using DesktopDatabase 
        
        if file already exists, parameters of config are loaded. 

        Args:
            path: path of config file to save to 
            intime: if True, setParam function will always save it to config file, if False, call to save is expected to write to file
        """
        self.path = path 
        self.intime = intime
        self.params = {}
        if os.path.exists(self.path):
            f = open(self.path, "r")
            self.params = json.loads(f.read())
            f.close()
    def save(self):
        """
        Write all parameters to config file in JSON format
        """
        f = open(self.path, "w")
        f.write(json.dumps(self.params))
        f.close()

    def setParam(self, k, v):
        """
        Sets parameter in config file. If intime in constructor is set to True, automatically writes to file. 
        
        Args:
            k: parameter name
            v: parameter value 
        """
        self.params[k]=v
        if self.intime:
            self.save()

    def getParam(self, k, default):
        """
        Gets parameter value from config

        Args:
            k: name of the parameter 
            default: default value is parameter is not present
        Returns:
            value of requested parameter or dedfault value if parameter is not specified. 
        """
        return self.params.get(k, default)
        
        
