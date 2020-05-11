from Tkinter import *
from tkFont import *

class LogIn(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        self.elements = {}

        title_frame = Frame(self)
        title_frame.pack(expand=True, fill=BOTH, padx=70, pady=(50, 20))

        title_font = Font(root=self, family='Arial', size=28)

        self.elements['title'] = Label(title_frame, text='Log In',
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

        password_frame = Frame(self)
        password_frame.pack(expand=True, fill=BOTH, padx=70, pady=(5, 10))

        self.elements['password_label'] = Label(password_frame, text='Password: ', font=label_font)
        self.elements['password_label'].pack(side=LEFT, padx=6)

        self.elements['password_entry'] = Entry(password_frame, font=entry_font, show='*')
        self.elements['password_entry'].pack(side=LEFT, padx=6, expand=True, fill=X)

        buttons_font = Font(root=self, family='Arial', size=16, weight=BOLD)

        buttons_frame = Frame(self)
        buttons_frame.pack(expand=True, fill=BOTH, padx=70, pady=(10, 0))

        self.elements['log_in_button'] = Button(buttons_frame, text='LOG IN',
            bg='#003399', activebackground='#002266', fg='#ffffff', font=buttons_font,
            activeforeground='#ffffff', command=self.log_in)
        self.elements['log_in_button'].pack(side=TOP, expand=True, fill=X, padx=6)

    def log_in(self):
        username = self.elements['username_entry'].get()
        password = self.elements['password_entry'].get()

        self.elements['username_entry'].delete(0, END)
        self.elements['password_entry'].delete(0, END)