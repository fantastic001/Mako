
from .BaseLogger import BaseLogger
import inspect

class Loggable:
    def __init__(self, obj, logger: BaseLogger) -> None:
        self.logger = logger
        self.obj = obj
    
    def __getattr__(self, attr):
        if callable(getattr(self.obj, attr)):
            self.logger.debug("%s called with:" % attr)
            def _callable(*args, **kw):
                self.logger.increase_debug_depth()
                for k, v in zip(inspect.getfullargspec(getattr(self.obj, attr))[0], [self.obj] + list(args)):
                    self.logger.debug("%s = %s" % (k, str(v)))
                for k,v in kw.items():
                    self.logger.debug("%s = %s" % (k, str(v)))
                result = getattr(self.obj, attr)(*args, **kw)
                self.logger.debug("Result = %s" % str(result))
                self.logger.decrease_debug_depth()
                return result
            return _callable

            