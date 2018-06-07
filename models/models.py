from abc import ABC, abstractmethod
import uuid
import time as t

class Model(ABC):
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

class User(Model):
    #type_ids = Buy - b, Seller - s, Admin - a'''
    __endpoint = 'users'

    def __init__(self, firstName, lastName, email, password, telephone = None, typeId = 's'):
        super().__init__()
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.telephone = telephone
        self.typeId = typeId
        self.uid = str(uuid.uuid4())
        self.uri = super(User, self).getBaseUri()
        self.password = password

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
            '_id': self.uid,
            'first_name': self.firstName,
            'last_name': self.lastName,
            'email': self.email,
            'password': self.password,
            'uri': self.uri + self.__endpoint + "/" + self.uid
        }

class Advert(Model):
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

class Rental(Model):
    __endpoint = 'rentals'
    def __init__(self, type, description, pictures = []):
        super().__init__()
        self.id = str(uuid.uuid4())
        self.description = description
        self.type = type
        self.pictures = pictures
        self.uri = super(Rental, self).getBaseUri()
        self.isPublished = False

    def getDescription(self):

        return self.description

    def setPublished(self, isPublished):
        self.isPublished = isPublished

    def serialize(self):

        return {
            '_id': self.id,
            'description': self.description,
            'type' : self.type,
            'pictures' : self.pictures,
            'published' : self.isPublished,
            'created': super(Rental, self).getCreated(),
            'uri': self.uri + self.__endpoint + "/" + self.id
        }