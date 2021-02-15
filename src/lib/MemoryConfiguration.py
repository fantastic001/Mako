
from . import Configuration

class MemoryConfiguration(Configuration):
    def __init__(self, data={}):
        self.data = data

    def open(self) -> dict:
        return self.data

    def save(self, params: dict):
        self.data = params
    