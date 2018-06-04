class User:
    def __init__(self, firstName, lastName):
        self.firstName = firstName
        self.lastName = lastName

    def getFirstName(self):

        return self.firstName

    def getLastName(self):

        return self.lastName

    def serialize(self):

        return {
            'first_name': self.firstName,
            'last_name': self.lastName
        }