from flask_httpauth import HTTPBasicAuth


class HttpBasicAuth:

    def authenticate(self):

        auth = HTTPBasicAuth()

        return auth

