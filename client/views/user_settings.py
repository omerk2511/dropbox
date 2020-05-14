from Tkinter import *

from common import Codes
from ..handlers.data import Data

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