
from .AMSBaseAction import * 

import os 
import subprocess 
import shlex


class AMSScriptAction(AMSBaseAction):
    """
    Measurement based on script output, either from standard output or via file

    Parameters:
    path: path to the script
    interpreter: interpreter to run script with (default: sh)
    result_as: path to the result, put 'stdout' for output from standard output
    args: list of arguments passed to the script (NOTE: this list is string, as you normaly pass arguments in the shell)
    """

    name = "os.script"

    def measure(self):
        path = self.getConfig().get("path", "script.sh")
        result = self.getConfig().get("result_as", "stdout")
        args = self.getConfig().get("args", "")
        interpreter = self.getConfig().get("interpreter", "sh")
        cmd = interpreter + " " + path + " " + args
        process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, cwd=os.getcwd())
        stdout, stderr = process.communicate()
        if result == "stdout":
            return float(stdout)
        else:
            f = open(result, "r")
            r = float(f.read())
            f.close()
            return r
