from Tkinter import *

from common import Codes
from ..controllers import LogInController
from ..handlers.data import Data

class LogIn(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        self.elements = {}

        title_frame = Frame(self)
        title_frame.pack(expand=True, fill=BOTH, padx=70, pady=(30, 20))

        self.elements['title'] = Label(title_frame, text='Log In',
            fg='#003399', font=('Arial', 28))
        self.elements['title'].pack(side=TOP)

        username_frame = Frame(self)
        username_frame.pack(expand=True, fill=BOTH, padx=70)

        self.elements['username_label'] = Label(username_frame, text='Username: ',
            font=('Arial', 18))
        self.elements['username_label'].pack(side=LEFT, padx=6)

        self.elements['username_entry'] = Entry(username_frame, font=('Arial', 18))
        self.elements['username_entry'].pack(side=LEFT, padx=6, expand=True, fill=X)

        password_frame = Frame(self)
        password_frame.pack(expand=True, fill=BOTH, padx=70, pady=(5, 10))

        self.elements['password_label'] = Label(password_frame, text='Password: ',
            font=('Arial', 18))
        self.elements['password_label'].pack(side=LEFT, padx=6)

        self.elements['password_entry'] = Entry(password_frame, font=('Arial', 18), show='*')
        self.elements['password_entry'].pack(side=LEFT, padx=6, expand=True, fill=X)

        buttons_frame = Frame(self)
        buttons_frame.pack(expand=True, fill=BOTH, padx=70, pady=(10, 0))

        self.elements['log_in_button'] = Button(buttons_frame, text='LOG IN',
            bg='#003399', activebackground='#002266', fg='#ffffff', font=('Arial', 16, 'bold'),
            activeforeground='#ffffff', command=self.log_in)
        self.elements['log_in_button'].pack(side=TOP, expand=True, fill=X, padx=6)

    def log_in(self):
        username = self.elements['username_entry'].get()
        password = self.elements['password_entry'].get()

        self.elements['username_entry'].delete(0, END)
        self.elements['password_entry'].delete(0, END)

        if len(username) == 0 or len(password) == 0:
            self.parent.display_error('You have to fill in all the fields.')
            return

        try:
            response = LogInController.log_in(username, password)

            if response.code == Codes.SUCCESS:
                Data().set_token(response.payload['token'])
                
                self.parent.display_info('Logged in successfully.')
                self.parent.set_root_frame('main')
            else:
                self.parent.display_error(response.payload['message'])
        except:
            self.parent.display_error('Connection timed out.')
            self.parent.quit()