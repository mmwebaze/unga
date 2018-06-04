import pymongo

class MongoDb:


    def __init__(self):
       self.client = pymongo.MongoClient()


    def getClient(self):

        return self.client
