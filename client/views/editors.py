from Tkinter import *

from common import Codes
from ..controllers import FileController # EditorController (?)
from ..handlers.data import Data

class Editors(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        self.elements = {}

        title_frame = Frame(self)
        title_frame.pack(expand=True, fill=BOTH, padx=70, pady=(30, 20))

        self.elements['title'] = Label(title_frame, text='Editors',
            fg='#003399', font=('Arial', 28))
        self.elements['title'].pack(side=TOP)

        self.elements['editors_frame'] = Frame(self)
        self.elements['editors_frame'].pack(side=TOP, padx=120, pady=30,
            expand=False, fill=BOTH)

        self.elements['new_editor_frame'] = Frame(self)
        self.elements['new_editor_frame'].pack(side=TOP, padx=120, pady=30,
            expand=False, fill=BOTH)

        self.elements['editor_frames'] = []
        
        self.current_file = None

    def initialize(self):
        self.current_file = Data().get_current_file()
        self.editors = FileController.get_file_editors(self.current_file, Data().get_token())
        
        for editor_frame in self.elements['editor_frames']:
            editor_frame.pack_forget()

        self.elements['editor_frames'] = []

        self.elements['editors_frame'].pack_forget()
        self.elements['editors_frame'].pack(side=TOP, padx=120, pady=30,
            expand=False, fill=BOTH)

        self.elements['new_editor_frame'].pack_forget()
        self.elements['new_editor_frame'].pack(side=TOP, padx=120, pady=(10, 30),
            expand=False, fill=BOTH)

        if not self.editors:
            no_editors_label = Label(self.elements['editors_frame'], bg='gray',
                text='There are no editors for this file.', font=('Arial', 22), anchor='w')
            no_editors_label.pack(side=LEFT, expand=True, fill=X)

            self.elements['editor_frames'].append(no_editors_label)

        for editor in self.editors:
            editor_frame = Frame(self.elements['editors_frame'], bg='gray')
            editor_frame.pack(side=TOP, expand=False, fill=X, pady=10)

            editor_label = Label(editor_frame, font=('Arial', 18), bg='gray',
                text='%s (%s)' % (editor['user']['username'], editor['user']['full_name']))
            editor_label.pack(side=LEFT, padx=20, pady=10)

            remove_editor_button = Button(editor_frame, text='Remove',
                font=('Arial', 16), bg='#990000', fg='#ffffff', activebackground='#b30000',
                activeforeground='#ffffff', command=self.generate_remove_editor(editor['id']))
            remove_editor_button.pack(side=RIGHT, padx=20, pady=10)

            self.elements['editor_frames'].append(editor_frame)

        if 'editor_entry' in self.elements:
            self.elements['editor_entry'].pack_forget()

        self.elements['editor_entry'] = Entry(self.elements['new_editor_frame'],
            font=('Arial', 18))
        self.elements['editor_entry'].pack(side=LEFT, padx=(0, 10), expand=True, fill=BOTH)

        if 'add_editor_button' in self.elements:
            self.elements['add_editor_button'].pack_forget()

        self.elements['add_editor_button'] = Button(self.elements['new_editor_frame'],
            text='Add Editor', font=('Arial', 18), bg='#003399', activebackground='#002266',
            fg='#ffffff', activeforeground='#ffffff', command=self.add_editor)
        self.elements['add_editor_button'].pack(side=LEFT, expand=False, fill=X)

    def add_editor(self):
        editor_username = self.elements['editor_entry'].get()
        self.elements['editor_entry'].delete(0, END)

        if not editor_username:
            self.parent.display_error('You have to enter an editor username.')
            return

        response = FileController.add_file_editor(self.current_file, editor_username,
            Data().get_token())

        if response.code == Codes.SUCCESS:
            self.parent.display_info('Editor added successfully!')
            self.initialize()
        else:
            self.parent.display_error(response.payload['message'])

    def generate_remove_editor(self, editor_id):
        return lambda: self.remove_editor(editor_id)

    def remove_editor(self, editor_id):
        response = FileController.remove_file_editor(editor_id, Data().get_token())

        if response.code == Codes.SUCCESS:
            self.parent.display_info('Editor removed successfully!')
            self.initialize()
        else:
            self.parent.display_error(response.payload['message'])