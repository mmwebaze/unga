from abc import ABC, abstractmethod
import uuid
import time as t

class Base(ABC):
    def __init__(self, baseUri = 'http://127.0.0.1:5000/unga/api/v1.0/'):
        self.baseUri = baseUri
        self.created = int(t.time())

    def getBaseUri(self):
        return self.baseUri

    def getCreated(self):

        return self.created

    @abstractmethod
    def serialize(self):
        pass
