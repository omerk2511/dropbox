from Tkinter import *
from tkFont import *

from common import Codes
from ..controllers import SignUpController

class SignUp(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        self.elements = {}

        title_frame = Frame(self)
        title_frame.pack(expand=True, fill=BOTH, padx=70, pady=(30, 20))

        title_font = Font(root=self, family='Arial', size=28)

        self.elements['title'] = Label(title_frame, text='Sign Up',
            fg='#003399', font=title_font)
        self.elements['title'].pack(side=TOP)

        label_font = Font(root=self, family='Arial', size=18)
        entry_font = Font(root=self, family='Arial', size=18)

        username_frame = Frame(self)
        username_frame.pack(expand=True, fill=BOTH, padx=70)

        self.elements['username_label'] = Label(username_frame, text='Username: ', font=label_font)
        self.elements['username_label'].pack(side=LEFT, padx=6)

        self.elements['username_entry'] = Entry(username_frame, font=entry_font)
        self.elements['username_entry'].pack(side=LEFT, padx=6, expand=True, fill=X)

        full_name_frame = Frame(self)
        full_name_frame.pack(expand=True, fill=BOTH, padx=70, pady=(5, 0))

        self.elements['full_name_label'] = Label(full_name_frame, text='Full Name: ', font=label_font)
        self.elements['full_name_label'].pack(side=LEFT, padx=6)

        self.elements['full_name_entry'] = Entry(full_name_frame, font=entry_font)
        self.elements['full_name_entry'].pack(side=LEFT, padx=6, expand=True, fill=X)

        password_frame = Frame(self)
        password_frame.pack(expand=True, fill=BOTH, padx=70, pady=(5, 10))

        self.elements['password_label'] = Label(password_frame, text='Password: ', font=label_font)
        self.elements['password_label'].pack(side=LEFT, padx=6)

        self.elements['password_entry'] = Entry(password_frame, font=entry_font, show='*')
        self.elements['password_entry'].pack(side=LEFT, padx=6, expand=True, fill=X)

        buttons_font = Font(root=self, family='Arial', size=16, weight=BOLD)

        buttons_frame = Frame(self)
        buttons_frame.pack(expand=True, fill=BOTH, padx=70, pady=(10, 0))

        self.elements['sign_up_button'] = Button(buttons_frame, text='SIGN UP',
            bg='#003399', activebackground='#002266', fg='#ffffff', font=buttons_font,
            activeforeground='#ffffff', command=self.sign_up)
        self.elements['sign_up_button'].pack(side=TOP, expand=True, fill=X, padx=6)

    def sign_up(self):
        username = self.elements['username_entry'].get()
        full_name = self.elements['full_name_entry'].get()
        password = self.elements['password_entry'].get()

        self.elements['username_entry'].delete(0, END)
        self.elements['full_name_entry'].delete(0, END)
        self.elements['password_entry'].delete(0, END)

        if len(username) == 0 or len(full_name) == 0 or len(password) == 0:
            self.parent.display_error('You have to fill in all the fields.')
            return

        try:
            response = SignUpController.sign_up(username, full_name, password)
        except:
            self.parent.display_error('Connection timed out.')
            self.parent.quit()

            return

        if response.code == Codes.SUCCESS:
            self.parent.display_info('Signed up successfully.')
            self.parent.return_frame()
        else:
            self.parent.display_error(response.payload['message'])