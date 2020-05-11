import jwt
import sqlite3 as lite

from common import Codes
from singleton import Singleton
from ..controllers import UserDataController

TOKEN_PATH = 'client/data/token.txt' # move to config

class Data(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.token = self.fetch_token()
        self.user_data = None

    def get_token(self):
        return self.token

    def set_token(self, token):
        self.token = token
        self.store_token(token)

    def get_user_data(self):
        return self.user_data

    def set_user_data(self):
        if self.token:
            try:
                user_data_response = UserDataController.get_user_data(self.token)

                if user_data_response.code != Codes.SUCCESS:
                    raise Exception('Not logged in.')

                self.user_data = user_data_response.payload
            except:
                self.token = None

    def fetch_token(self):
        try:
            with open(TOKEN_PATH, 'r') as f:
                return f.read().strip()
        except:
            return None

    def store_token(self, token):
        with open(TOKEN_PATH, 'w') as f:
            f.write(token)