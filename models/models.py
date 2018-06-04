from abc import ABC, abstractmethod

class Model(ABC):
    def __init__(self, baseUri = 'http://127.0.0.1:5000/unga/api/v1.0/'):
        self.baseUri = baseUri
    #@abstractmethod
    def getBaseUri(self):
        return self.baseUri

    @abstractmethod
    def serialize(self):
        pass

"""class User(Model):
    #type_ids = Buy - b, Seller - s, Admin - a'''

    def __init__(self, firstName, lastName, email, telephone = None, typeId = 's'):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.telephone = telephone
        self.typeId = typeId

    def getFirstName(self):

        return self.firstName

    def setFirstName(self, firstName):
        self.firstName = firstName

    def getLastName(self):

        return self.lastName

    def setLastName(self, lastName):
        self.lastName = lastName

    def getEmail(self):

        return self.email

    def setEmail(self, email):
        self.email = email

    def getTelephone(self):

        return self.telephone

    def setTelephone(self, telephone):

        self.telephone = telephone

    def serialize(self):

        return {
            'first_name': self.firstName,
            'last_name': self.lastName
        }
"""
class Advert(Model):
    endpoint = 'adverts'
    def __init__(self, advertId, message, promocode = None):
        super().__init__()
        self.advertId = advertId
        self.advertMessage = message
        self.promocode = promocode
        self.uri = super(Advert, self).getBaseUri()
        #self.uri = super()

    def getAdvertId(self):

        return self.advertId

    def getAdvertMessage(self):

        return self.advertMessage+" "+self.promocode

    def setAdvertMessage(self, message):

        self.advertMessage = message

    def serialize(self):

        return {
            'id': str(self.advertId),
            'message': self.advertMessage,
            'uri': self.uri+self.endpoint+"/"+str(self.advertId)
        }

class Rental(Model):

    @abstractmethod
    def rentalPictures(self):
        pass