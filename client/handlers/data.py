import jwt
import sqlite3 as lite

from singleton import Singleton

TOKEN_PATH = 'client/data/token.txt' # move to config

class Data(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.token = self.fetch_token()

    def get_token(self):
        return self.token

    def set_token(self, token):
        self.token = token
        self.store_token(token)

    def fetch_token(self):
        try:
            with open(TOKEN_PATH, 'r') as f:
                return f.read().strip()
        except:
            return None

    def store_token(self, token):
        with open(TOKEN_PATH, 'w') as f:
            f.write(token)