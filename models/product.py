from models.base import Base
import uuid

class Product(Base):
    __endpoint = 'products'
    def __init__(self, type, description, pictures = []):
        super().__init__()
        self.id = str(uuid.uuid4())
        self.description = description
        self.type = type
        self.pictures = pictures
        self.uri = super(Product, self).getBaseUri()
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
            'created': super(Product, self).getCreated(),
            'uri': self.uri + self.__endpoint + "/" + self.id
        }