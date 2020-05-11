from Tkinter import Tk, Frame
from tkMessageBox import showinfo, showerror

from data import Data
from ..views import Home, LogIn, SignUp, Main

WIDTH = 600
HEIGHT = 320

TITLE = 'Dropbox'

class GUI(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.geometry('%dx%d' % (WIDTH, HEIGHT))
        self.resizable(False, False)

        self.title(TITLE)

        self.bind('<Escape>', self.return_frame)

        self.frames = {
            Home: Home(self),
            Main: Main(self),
            LogIn: LogIn(self),
            SignUp: SignUp(self)
        }

        self.frame_stack = []

        if Data().get_token():
            self.show_frame(Main)
        else:
            self.show_frame(Home)

    def show_frame(self, frame):
        self.frames[frame].grid(row=0, column=0, sticky='NSEW')
        self.frames[frame].tkraise()

        self.frame_stack.append(frame)

    def set_root_frame(self, frame):
        self.frame_stack = []
        self.show_frame(frame)

    def return_frame(self, event=None):
        if len(self.frame_stack) == 1:
            return

        frame = self.frame_stack[-2]
        self.frame_stack = self.frame_stack[:-2]

        self.show_frame(frame)

    def display_info(self, info_message):
        showinfo('Info', info_message)

    def display_error(self, error_message):
        showerror('Error!', error_message)