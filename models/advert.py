from models.base import Base
import uuid

class Advert(Base):
    __endpoint = 'adverts'
    def __init__(self, message, promocode = None):
        super().__init__()
        self.advertId = str(uuid.uuid4())
        self.advertMessage = message
        self.promocode = promocode
        self.isPublished = False
        self.uri = super(Advert, self).getBaseUri()

    def getAdvertId(self):

        return self.advertId

    def getAdvertMessage(self):

        return self.advertMessage+" "+self.promocode

    def setAdvertMessage(self, message):

        self.advertMessage = message

    def serialize(self):

        return {
            '_id': self.advertId,
            'message': self.advertMessage,
            'published': self.isPublished,
            'created': super(Advert, self).getCreated(),
            'uri': self.uri+self.__endpoint+"/"+self.advertId
        }