from Tkinter import *
from tkFont import *

from log_in import LogIn
from sign_up import SignUp

class Home(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        self.elements = {}

        title_frame = Frame(self)
        title_frame.pack(expand=True, fill=BOTH, padx=70, pady=(50, 30))

        title_font = Font(root=self, family='Arial', size=34)

        self.elements['title'] = Label(title_frame, text='Welcome to Dropbox!',
            fg='#003399', font=title_font)
        self.elements['title'].pack(side=TOP, padx=6)

        buttons_frame = Frame(self)
        buttons_frame.pack(expand=True, fill=BOTH, padx=70, pady=(0, 10))

        buttons_font = Font(root=self, family='Arial', size=20, weight=BOLD)

        self.elements['log_in_button'] = Button(buttons_frame, text='LOG IN',
            bg='#003399', activebackground='#002266', fg='#ffffff', font=buttons_font,
            activeforeground='#ffffff', width=12, height=3, command=self.log_in)
        self.elements['log_in_button'].pack(side=LEFT, padx=6)

        self.elements['sign_up_button'] = Button(buttons_frame, text='SIGN UP',
            bg='#ffffff', activebackground='#f2f2f2', fg='#003399', font=buttons_font,
            activeforeground='#003399', width=12, height=3, command=self.sign_up)
        self.elements['sign_up_button'].pack(side=RIGHT, padx=6)

    def log_in(self):
        self.parent.show_frame(LogIn)

    def sign_up(self):
        self.parent.show_frame(SignUp)