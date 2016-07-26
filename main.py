import falcon
import mysql.connector
#from note import NoteCategory, NoteIndex
from log import LogCategory, LogIndex
from user import User

cnx = mysql.connector.connect(user='api', password='apiapi', host='127.0.0.1', database='apis')
cursor = cnx.cursor()

class AuthMiddleware(object):
    def process_request(self, req, resp):
        token = req.get_header('Authorization')
        account_id = req.get_header('Account-ID')
        challenges = ['Token type="Fernet"']
        if token is None:
            description = ('Please provide an auth token as part of the request.')
            raise falcon.HTTPUnauthorized('Auth token required',
                description,
                challenges,
                href='http://docs.example.com/auth')
        if not self._token_is_valid(token, account_id):
            description = ('The provided auth token is not valid. Please request a new token and try again.')
            raise falcon.HTTPUnauthorized('Authentication required',
                    description,
                    challenges,
                    href='http://docs.example.com/auth')
    def _token_is_valid(self, token, account_id):
        return True

api = falcon.API()
api.add_route('/user/', User(cnx, cursor))
#api.add_route('/notes/', NoteCategory(cnx, cursor))
#api.add_route('/notes/{index}/', NoteIndex(cnx, cursor))
api.add_route('/logs/', LogCategory(cnx, cursor))
api.add_route('/logs/{index}/', LogIndex(cnx, cursor))
