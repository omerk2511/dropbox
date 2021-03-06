import jwt
import sqlite3 as lite

from common import Codes
from singleton import Singleton
from ..controllers import UserController, GroupController

TOKEN_PATH = 'client/data/token.txt' # move to config

class Data(object):
    __metaclass__ = Singleton

    def __init__(self):
        """
        Initializes a Data object
        args: self
        ret: none
        """

        self.token = self.fetch_token()
        self.user_data = None
        self.current_group = None
        self.current_file = None

    def get_token(self):
        """
        Gets the current token
        args: self
        ret: token
        """

        return self.token

    def set_token(self, token):
        """
        Sets the current token
        args: self, token
        ret: none
        """

        self.token = token
        self.store_token(token)

    def get_current_group(self):
        """
        Gets the current group
        args: self
        ret: group
        """

        if self.current_group and self.token:
            group_data_response = GroupController.get_group_data(
                self.current_group, self.token)

            if group_data_response.code != Codes.SUCCESS:
                raise Exception(group_data_response.payload['message'])

            return group_data_response.payload

    def set_current_group(self, group):
        """
        Sets the current group
        args: self, group
        ret: none
        """

        self.current_group = group

    def get_current_file(self):
        """
        Gets the current file
        args: self
        ret: file
        """

        return self.current_file

    def set_current_file(self, current_file):
        """
        Sets the current file
        args: self, current_file
        ret: none
        """

        self.current_file = current_file

    def get_user_data(self):
        """
        Gets the current user data
        args: self
        ret: user_data
        """

        return self.user_data

    def get_file_info(self, group, file_id):
        """
        Gets the information of a file
        args: self, group, file_id
        ret: file_info
        """

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
        """
        Gets the information of a directory
        args: self, group, file_id
        ret: directory_info
        """

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
        """
        Sets the current user data
        args: none
        ret: none
        """

        if self.token:
            try:
                user_data_response = UserController.get_user_data(self.token)

                if user_data_response.code != Codes.SUCCESS:
                    raise Exception('Not logged in.')

                self.user_data = user_data_response.payload
            except:
                self.token = None

    def fetch_token(self):
        """
        Fetches the token from a file
        args: self
        ret: token
        """

        try:
            with open(TOKEN_PATH, 'r') as f:
                return f.read().strip()
        except:
            return None

    def store_token(self, token):
        """
        Stores a token into a file
        args: self, token
        ret: none
        """

        with open(TOKEN_PATH, 'w') as f:
            f.write(token)