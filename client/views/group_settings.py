from Tkinter import *

from common import Codes
from ..handlers.data import Data
from ..controllers import GroupController

class GroupSettings(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        self.elements = {}
        
        title_frame = Frame(self)
        title_frame.pack(expand=True, fill=BOTH, padx=70, pady=(30, 20))

        self.elements['title'] = Label(title_frame, text='Settings',
            fg='#003399', font=('Arial', 28))
        self.elements['title'].pack(side=TOP)

        group_name_frame = Frame(self)
        group_name_frame.pack(expand=True, fill=BOTH, padx=70)

        self.elements['group_name_label'] = Label(group_name_frame, text='Group Name: ',
            font=('Arial', 18))
        self.elements['group_name_label'].pack(side=LEFT, padx=6)

        self.elements['group_name_entry'] = Entry(group_name_frame, font=('Arial', 18))
        self.elements['group_name_entry'].pack(side=LEFT, padx=6, expand=True, fill=X)

        buttons_frame = Frame(self)
        buttons_frame.pack(expand=True, fill=BOTH, padx=70, pady=(10, 0))

        self.elements['update_group_name_button'] = Button(buttons_frame, text='UPDATE',
            bg='#003399', activebackground='#002266', fg='#ffffff', font=('Arial', 16, 'bold'),
            activeforeground='#ffffff', command=self.update_group_name)
        self.elements['update_group_name_button'].pack(side=TOP, expand=True, fill=X, padx=6)

        self.elements['group_users_frame'] = Frame(self)
        self.elements['group_users_frame'].pack(expand=True, fill=BOTH, padx=70, pady=40)

        self.elements['group_user_frames'] = []

    def initialize(self):
        self.current_group_data = Data().get_current_group()

        for group_user_frame in self.elements['group_user_frames']:
            group_user_frame.pack_forget()

        self.elements['group_user_frames'] = []

        self.elements['group_users_frame'].pack_forget()
        self.elements['group_users_frame'].pack(expand=True, fill=BOTH, padx=70, pady=40)

        users = self.current_group_data['users']

        for user in users:
            user_frame = Frame(self.elements['group_users_frame'], bg='gray')
            user_frame.pack(side=TOP, expand=False, fill=X, pady=10)

            user_label = Label(user_frame, font=('Arial', 18), bg='gray',
                text='%s (%s)' % (user['username'], user['full_name']))
            user_label.pack(side=LEFT, padx=20, pady=10)

            if user['id'] != Data().get_user_data()['id']:
                transfer_ownership_button = Button(user_frame, text='Transfer Ownership',
                    font=('Arial', 16), bg='#004d00', fg='#ffffff', activebackground='#006600',
                    activeforeground='#ffffff', command=self.generate_transfer_ownership(user['id']))
                transfer_ownership_button.pack(side=RIGHT, padx=20, pady=10)

                kick_user_button = Button(user_frame, text='Kick User',
                    font=('Arial', 16), bg='#990000', fg='#ffffff', activebackground='#b30000',
                    activeforeground='#ffffff', command=self.generate_kick_user(user['id']))
                kick_user_button.pack(side=RIGHT, pady=10)

            self.elements['group_user_frames'].append(user_frame)

    def generate_transfer_ownership(self, user_id):
        return lambda: self.transfer_ownership(user_id)

    def generate_kick_user(self, user_id):
        return lambda: self.kick_user(user_id)

    def transfer_ownership(self, user_id):
        response = GroupController.update_group(self.current_group_data['id'],
            Data().get_token(), owner=user_id)

        if response.code == Codes.SUCCESS:
            self.parent.display_info('The group ownership has been transferred successfully!')
            self.parent.return_frame()
        else:
            self.parent.display_error(response.payload['message'])

    def kick_user(self, user_id):
        print 'kicking user', user_id

    def update_group_name(self):
        group_name = self.elements['group_name_entry'].get()
        self.elements['group_name_entry'].delete(0, END)

        if group_name:
            response = GroupController.update_group(self.current_group_data['id'],
                Data().get_token(), name=group_name)

            if response.code == Codes.SUCCESS:
                self.parent.display_info('The group name has been updated successfully!')
            else:
                self.parent.display_error(response.payload['message'])
        else:
            self.parent.display_error('You have to enter a group name.')