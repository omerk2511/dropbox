import jwt
import sqlite3 as lite

from common import Codes
from singleton import Singleton
from ..controllers import UserController, GroupController

TOKEN_PATH = 'client/data/token.txt' # move to config

class Data(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.token = self.fetch_token()
        self.user_data = None
        self.current_group = None
        self.current_file = None

    def get_token(self):
        return self.token

    def set_token(self, token):
        self.token = token
        self.store_token(token)

    def get_current_group(self):
        if self.current_group and self.token:
            group_data_response = GroupController.get_group_data(
                self.current_group, self.token)

            if group_data_response.code != Codes.SUCCESS:
                raise Exception(group_data_response.payload['message'])

            return group_data_response.payload

    def set_current_group(self, group):
        self.current_group = group

    def get_current_file(self):
        return self.current_file

    def set_current_file(self, current_file):
        self.current_file = current_file

    def get_user_data(self):
        return self.user_data

    def get_file_info(self, group, file_id):
        files = [group['files']]
        
        while files:
            if files[0]['type'] == 'directory':
                files += files[0]['files']
            else:
                if files[0]['id'] == file_id:
                    f = files[0].copy()
                    
                    if 'users' in group:
                        owner = [user for user in group['users'] if user['id'] == f['owner']][0]

                        f['owner'] = {
                            'id': owner['id'],
                            'username': owner['username'],
                            'full_name': owner['full_name']
                        }
                    else:
                        f['owner'] = {
                            'id': group['id'],
                            'username': group['username'],
                            'full_name': group['full_name']
                        }

                    return f

            files = files[1:]

    def get_directory_info(self, group, directory_id):
        files = [group['files']]
        
        while files:
            if files[0]['type'] == 'directory':
                if files[0]['id'] == directory_id:
                    directory = files[0].copy()

                    if 'users' in group:
                        owner = [user for user in group['users'] if user['id'] == directory['owner']][0]

                        directory['owner'] = {
                            'id': owner['id'],
                            'username': owner['username'],
                            'full_name': owner['full_name']
                        }
                    else:
                        directory['owner'] = {
                            'id': group['id'],
                            'username': group['username'],
                            'full_name': group['full_name']
                        }

                    return directory

                files += files[0]['files']

            files = files[1:]

    def set_user_data(self):
        if self.token:
            try:
                user_data_response = UserController.get_user_data(self.token)

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