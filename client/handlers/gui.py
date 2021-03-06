from Tkinter import Tk, Frame, BOTH
from tkMessageBox import showinfo, showerror

from data import Data
from ..views import *

WIDTH = 1200
HEIGHT = 790

TITLE = 'Dropbox'

class GUI(Tk):
    def __init__(self, *args, **kwargs):
        """
        Creates a GUI object
        args: self, *args, **kwargs
        ret: none
        """

        Tk.__init__(self, *args, **kwargs)

        self.geometry('%dx%d' % (WIDTH, HEIGHT))
        self.resizable(False, False)

        self.title(TITLE)

        self.bind('<Escape>', self.return_frame)

    def initialize_frames(self):
        """
        Initializes all the frames
        args: self
        ret: none
        """

        self.frames = {
            'home': Home(self),
            'main': Main(self),
            'log_in': LogIn(self),
            'sign_up': SignUp(self),
            'user_settings': UserSettings(self),
            'group_settings': GroupSettings(self),
            'user_invites': UserInvites(self),
            'group_invites': GroupInvites(self),
            'editors': Editors(self),
            'admin': Admin(self)
        }

        self.frame_stack = []

        Data().set_user_data()

        if Data().get_token():
            self.show_frame('main')
        else:
            self.show_frame('home')

    def show_frame(self, frame):
        """
        Shows a frame
        args: self, frame
        ret: none
        """

        if self.frame_stack:
            self.frames[self.frame_stack[-1]].pack_forget()

        try:
            self.frames[frame].initialize()
        except:
            pass

        self.frames[frame].pack(expand=False, fill=BOTH)
        self.frames[frame].tkraise()

        self.frame_stack.append(frame)

    def set_root_frame(self, frame):
        """
        Sets a root frame
        args: self, frame
        ret: none
        """

        if self.frame_stack:
            self.frames[self.frame_stack[-1]].pack_forget()

        self.frame_stack = []
        self.show_frame(frame)

    def return_frame(self, event=None):
        """
        Returns a frame back
        args: self, event
        ret: none
        """

        if len(self.frame_stack) == 1:
            return

        self.frames[self.frame_stack[-1]].pack_forget()

        frame = self.frame_stack[-2]
        self.frame_stack = self.frame_stack[:-2]

        self.show_frame(frame)

    def display_info(self, info_message):
        """
        Displays an information pop up
        args: self, info_message
        ret: none
        """

        showinfo('Info', info_message)

    def display_error(self, error_message):
        """
        Displays an error pop up
        args: self, error_message
        ret: none
        """

        showerror('Error!', error_message)