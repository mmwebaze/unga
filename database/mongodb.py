import pymongo

class MongoDb:

    def __init__(self, host = "localhost", port = 27017):
       self.client = pymongo.MongoClient(host, port)


    def getClient(self):

        return self.client
