from Tkinter import Tk, Frame
from tkMessageBox import showerror

from ..views import Home, LogIn, SignUp

WIDTH = 600
HEIGHT = 320

TITLE = 'Dropbox'

class GUI(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.geometry('%dx%d' % (WIDTH, HEIGHT))
        self.resizable(False, False)

        self.title(TITLE)

        self.frames = {
            Home: Home(self),
            LogIn: LogIn(self),
            SignUp: SignUp(self)
        }

        self.show_frame(Home)

    def show_frame(self, frame):
        self.frames[frame].grid(row=0, column=0, sticky='NSEW')
        self.frames[frame].tkraise()

    def display_error(self, error_message):
        showerror('Error!', error_message)