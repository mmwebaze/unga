from flask_httpauth import HTTPBasicAuth


class HttpBasicAuth:

    def authenticate(self):

        auth = HTTPBasicAuth()

        return auth

    def verifyCredentials(self, username, password, db):


        return []