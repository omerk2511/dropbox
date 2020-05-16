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

    def initialize(self):
        self.current_group_data = Data().get_current_group()

        # display the users

    def update_group_name(self):
        group_name = self.elements['group_name_entry'].get()
        self.elements['group_name_entry'].delete(0, END)

        if group_name:
            response = GroupController.update_group(self.current_group_data['id'],
                Data().get_token(), group_name)

            if response.code == Codes.SUCCESS:
                self.parent.display_info('The group name has been updated successfully!')
            else:
                self.parent.display_error(response.payload['message'])
        else:
            self.parent.display_error('You have to enter a group name.')