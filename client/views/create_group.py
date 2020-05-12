from Tkinter import *
from tkFont import *

from common import Codes
from ..controllers import GroupController
from ..handlers.data import Data

class CreateGroup(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        self.elements = {}

        title_frame = Frame(self)
        title_frame.pack(expand=True, fill=BOTH, padx=70, pady=(30, 20))

        title_font = Font(root=self, family='Arial', size=28)

        self.elements['title'] = Label(title_frame, text='Create Group',
            fg='#003399', font=title_font)
        self.elements['title'].pack(side=TOP)

        label_font = Font(root=self, family='Arial', size=18)
        entry_font = Font(root=self, family='Arial', size=18)

        group_name_frame = Frame(self)
        group_name_frame.pack(expand=True, fill=BOTH, padx=70)

        self.elements['group_name_label'] = Label(group_name_frame, text='Group Name: ', font=label_font)
        self.elements['group_name_label'].pack(side=LEFT, padx=6)

        self.elements['group_name_entry'] = Entry(group_name_frame, font=entry_font)
        self.elements['group_name_entry'].pack(side=LEFT, padx=6, expand=True, fill=X)

        buttons_font = Font(root=self, family='Arial', size=16, weight=BOLD)

        buttons_frame = Frame(self)
        buttons_frame.pack(expand=True, fill=BOTH, padx=70, pady=(10, 0))

        self.elements['create_group_button'] = Button(buttons_frame, text='CREATE GROUP',
            bg='#003399', activebackground='#002266', fg='#ffffff', font=buttons_font,
            activeforeground='#ffffff', command=self.create_group)
        self.elements['create_group_button'].pack(side=TOP, expand=True, fill=X, padx=6)

    def create_group(self):
        group_name = self.elements['group_name_entry'].get()
        self.elements['group_name_entry'].delete(0, END)

        if len(group_name) == 0:
            self.parent.display_error('You have to provide a group name.')
            return

        try:
            response = GroupController.create_group(group_name, Data().get_token())
        except:
            self.parent.display_error('Connection timed out.')
            self.parent.quit()

        if response.code == Codes.SUCCESS:          
            self.parent.display_info('Created a group successfully.')
            self.parent.return_frame()
        else:
            self.parent.display_error(response.payload['message'])