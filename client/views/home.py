from Tkinter import *

class Home(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        self.elements = {}

        title_frame = Frame(self)
        title_frame.pack(expand=True, fill=BOTH, padx=70, pady=(50, 30))

        self.elements['title'] = Label(title_frame, text='Welcome to Dropbox!',
            fg='#003399', font=('Arial', 34))
        self.elements['title'].pack(side=TOP, padx=6)

        buttons_frame = Frame(self)
        buttons_frame.pack(expand=True, fill=BOTH, padx=70, pady=(0, 10))

        self.elements['log_in_button'] = Button(buttons_frame, text='LOG IN',
            bg='#003399', activebackground='#002266', fg='#ffffff', font=('Arial', 20, 'bold'),
            activeforeground='#ffffff', command=self.log_in)
        self.elements['log_in_button'].pack(side=LEFT, padx=6, expand=True, fill=BOTH)

        self.elements['sign_up_button'] = Button(buttons_frame, text='SIGN UP',
            bg='#ffffff', activebackground='#f2f2f2', fg='#003399', font=('Arial', 20, 'bold'),
            activeforeground='#003399', command=self.sign_up)
        self.elements['sign_up_button'].pack(side=RIGHT, padx=6, expand=True, fill=BOTH)

    def log_in(self):
        self.parent.show_frame('log_in')

    def sign_up(self):
        self.parent.show_frame('sign_up')