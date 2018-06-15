from models.base import Base
import uuid

class User(Base):
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

    def getUid(self):

        return self.uid

    def serialize(self):

        return {
            '_id': self.uid,
            'first_name': self.firstName,
            'last_name': self.lastName,
            'email': self.email,
            'password': self.password,
            'uri': self.uri + self.__endpoint + "/" + self.uid
        }