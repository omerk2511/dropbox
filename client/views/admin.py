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

        errors_scrollbar = Scrollbar(errors_frame)
        errors_scrollbar.pack(side=RIGHT, fill=Y)

        self.elements['errors_listbox'] = Listbox(errors_frame, font=('Arial', 14),
            yscrollcommand=errors_scrollbar.set)
        self.elements['errors_listbox'].pack(side=TOP, anchor=NW, expand=True, fill=BOTH)

        requests_frame = Frame(self)
        requests_frame.pack(expand=True, fill=BOTH, padx=70, pady=(15, 40))

        self.elements['requests_label'] = Label(requests_frame, text='Requests:',
            font=('Arial', 18))
        self.elements['requests_label'].pack(side=TOP, anchor=NW, pady=5)

        requests_scrollbar = Scrollbar(requests_frame)
        requests_scrollbar.pack(side=RIGHT, fill=Y)

        self.elements['requests_listbox'] = Listbox(requests_frame, font=('Arial', 14),
            yscrollcommand=requests_scrollbar.set)
        self.elements['requests_listbox'].pack(side=TOP, anchor=NW, expand=True, fill=BOTH)

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
        self.elements['requests_listbox'].delete(0, END)

        for log in self.admin_data['logs']:
            if log['type'] == 'error':
                self.elements['errors_listbox'].insert(END, log['message'])
            elif log['type'] == 'request':
                self.elements['requests_listbox'].insert(END, log['message'])