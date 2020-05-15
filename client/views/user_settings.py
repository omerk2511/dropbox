from Tkinter import *

from common import Codes
from ..handlers.data import Data
from ..controllers import UserController

class UserSettings(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        self.elements = {}
        
        title_frame = Frame(self)
        title_frame.pack(expand=True, fill=BOTH, padx=70, pady=(30, 20))

        self.elements['title'] = Label(title_frame, text='Settings',
            fg='#003399', font=('Arial', 28))
        self.elements['title'].pack(side=TOP)

        full_name_frame = Frame(self)
        full_name_frame.pack(expand=True, fill=BOTH, padx=70)

        self.elements['full_name_label'] = Label(full_name_frame, text='Full Name: ',
            font=('Arial', 18))
        self.elements['full_name_label'].pack(side=LEFT, padx=6)

        self.elements['full_name_entry'] = Entry(full_name_frame, font=('Arial', 18))
        self.elements['full_name_entry'].pack(side=LEFT, padx=6, expand=True, fill=X)

        password_frame = Frame(self)
        password_frame.pack(expand=True, fill=BOTH, padx=70, pady=(5, 10))

        self.elements['password_label'] = Label(password_frame, text='Password: ',
            font=('Arial', 18))
        self.elements['password_label'].pack(side=LEFT, padx=6)

        self.elements['password_entry'] = Entry(password_frame, font=('Arial', 18), show='*')
        self.elements['password_entry'].pack(side=LEFT, padx=6, expand=True, fill=X)

        buttons_frame = Frame(self)
        buttons_frame.pack(expand=True, fill=BOTH, padx=70, pady=(10, 0))

        self.elements['update_settings_button'] = Button(buttons_frame, text='UPDATE SETTINGS',
            bg='#003399', activebackground='#002266', fg='#ffffff', font=('Arial', 16, 'bold'),
            activeforeground='#ffffff', command=self.update_settings)
        self.elements['update_settings_button'].pack(side=TOP, expand=True, fill=X, padx=6)

    def update_settings(self):
        full_name = self.elements['full_name_entry'].get()
        password = self.elements['password_entry'].get()

        self.elements['full_name_entry'].delete(0, END)
        self.elements['password_entry'].delete(0, END)

        if not full_name and not password:
            self.parent.display_error('You have to enter a full name or a password.')
            return

        try:
            response = UserController.update_user(Data().get_token(), full_name, password)

            if response.code == Codes.SUCCESS:                
                self.parent.display_info('User settings updated successfully.')
                Data().set_token(response.payload['token'])
            else:
                self.parent.display_error(response.payload['message'])
        except:
            self.parent.display_error('Connection timed out.')
            self.parent.quit()