from Tkinter import *
from tkFont import *

class LogIn(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        self.elements = {}

        title_frame = Frame(self)
        title_frame.pack(expand=True, fill=BOTH, padx=70, pady=(50, 30))

        title_font = Font(root=self, family='Arial', size=24)

        self.elements['title'] = Label(title_frame, text='Log In',
            fg='#003399', font=title_font)
        self.elements['title'].pack(side=TOP)

        form_frame = Frame(self)
        form_frame.pack(expand=True, fill=BOTH, padx=70, pady=(0, 10))

        form_font = Font(root=self, family='Arial', size=16)

        self.elements['username_label'] = Label(form_frame, text='Username', font=form_font)
        self.elements['username_label'].pack(side=LEFT, padx=6)