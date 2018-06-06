class User:
    def __init__(self, firstName, lastName, password, email):
        self.firstName = firstName
        self.lastName = lastName
        self.password = password
        self.email = email

    def getFirstName(self):

        return self.firstName

    def getLastName(self):

        return self.lastName

    def serialize(self):

        return {
            'first_name': self.firstName,
            'last_name': self.lastName
        }