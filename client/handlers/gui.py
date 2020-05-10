from Tkinter import Tk, Frame

WIDTH = 500
HEIGHT = 300

TITLE = 'Dropbox'

class GUI(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.geometry('%dx%d' % (WIDTH, HEIGHT))
        self.resizable(False, False)

        self.title(TITLE)

        self.frames = {
            
        }

        self.show_frame()

    def show_frame(self, frame):
        self.frames[frame].grid(row=0, column=0, sticky='NSEW')
        self.frames[frame].tkraise()