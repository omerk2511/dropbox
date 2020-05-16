from Tkinter import *

from common import Codes
from ..controllers import AdminDataController
from ..handlers.data import Data

class Admin(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        self.elements = {}

        title_frame = Frame(self)
        title_frame.pack(expand=True, fill=BOTH, padx=70, pady=(30, 15))

        self.elements['title'] = Label(title_frame, text='Admin',
            fg='#003399', font=('Arial', 28))
        self.elements['title'].pack(side=TOP)

        used_space_frame = Frame(self)
        used_space_frame.pack(expand=True, fill=BOTH, padx=70, pady=30)

        self.elements['used_space_label'] = Label(used_space_frame, text='Used Space: ',
            font=('Arial', 18))
        self.elements['used_space_label'].pack(side=LEFT)

        errors_frame = Frame(self)
        errors_frame.pack(expand=True, fill=BOTH, padx=70, pady=(0, 15))

        self.elements['errors_label'] = Label(errors_frame, text='Errors:',
            font=('Arial', 18))
        self.elements['errors_label'].pack(side=TOP, anchor=NW, pady=5)

        y_errors_scrollbar = Scrollbar(errors_frame)
        y_errors_scrollbar.pack(side=RIGHT, fill=Y)

        x_errors_scrollbar = Scrollbar(errors_frame, orient='horizontal')
        x_errors_scrollbar.pack(side=BOTTOM, fill=X)        

        self.elements['errors_listbox'] = Listbox(errors_frame, font=('Arial', 14),
            yscrollcommand=y_errors_scrollbar.set, xscrollcommand=x_errors_scrollbar.set)
        self.elements['errors_listbox'].pack(side=TOP, anchor=NW, expand=True, fill=BOTH)

        y_errors_scrollbar.config(command=self.elements['errors_listbox'].yview)
        x_errors_scrollbar.config(command=self.elements['errors_listbox'].xview)

        activity_frame = Frame(self)
        activity_frame.pack(expand=True, fill=BOTH, padx=70, pady=(15, 40))

        self.elements['activity_label'] = Label(activity_frame, text='Activity:',
            font=('Arial', 18))
        self.elements['activity_label'].pack(side=TOP, anchor=NW, pady=5)

        y_activity_scrollbar = Scrollbar(activity_frame)
        y_activity_scrollbar.pack(side=RIGHT, fill=Y)

        x_activity_scrollbar = Scrollbar(activity_frame, orient='horizontal')
        x_activity_scrollbar.pack(side=BOTTOM, fill=X)

        self.elements['activity_listbox'] = Listbox(activity_frame, font=('Arial', 14),
            yscrollcommand=y_activity_scrollbar.set, xscrollcommand=x_activity_scrollbar.set)
        self.elements['activity_listbox'].pack(side=TOP, anchor=NW, expand=True, fill=BOTH)

        y_activity_scrollbar.config(command=self.elements['activity_listbox'].yview)
        x_activity_scrollbar.config(command=self.elements['activity_listbox'].xview)

    def initialize(self):
        admin_data_response = AdminDataController.get_admin_data(Data().get_token())

        if admin_data_response.code != Codes.SUCCESS:
            self.parent.display_error(admin_data_response.payload['message'])
            self.parent.return_frame()
            return

        self.admin_data = admin_data_response.payload

        self.elements['used_space_label']['text'] = 'Used Space: ' + str(
            self.admin_data['used_space']) + 'MB'

        self.elements['errors_listbox'].delete(0, END)
        self.elements['activity_listbox'].delete(0, END)

        for log in self.admin_data['logs']:
            if log['type'] == 'error':
                self.elements['errors_listbox'].insert(END, log['message'])
            elif log['type'] == 'activity':
                self.elements['activity_listbox'].insert(END, log['message'])