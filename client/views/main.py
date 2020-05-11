from Tkinter import *
from tkFont import *

class Main(Frame):
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