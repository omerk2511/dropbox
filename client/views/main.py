from Tkinter import *
from tkFont import *

from ..handlers.data import Data
from ..controllers import GroupDataController

class Main(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        self.elements = {}

    def initialize(self):
        Data().set_user_data()
        self.user_data = Data().get_user_data()

        if self.elements:
            # update the user data based elements

            self.elements['title']['text'] = 'Dropbox - ' + self.user_data['username']

            self.elements['groups_listbox'].delete(0, END)

            for group in ['Personal'] + [group['name'] for group in self.user_data['groups']]:
                self.elements['groups_listbox'].insert(END, group)

            self.elements['groups_listbox'].select_set(0)
            self.elements['groups_listbox'].event_generate('<<ListboxSelect>>')

            return
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=200)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)

        top_frame = Frame(self, bg='#003399')
        top_frame.grid(row=0, columnspan=2, sticky='NEW')

        # LOGO

        title_font = Font(root=self, family='Arial', size=22)

        self.elements['title'] = Label(top_frame, text='Dropbox - ' + self.user_data['username'],
            padx=10, pady=10, fg='#ffffff', bg='#003399', font=title_font)
        self.elements['title'].pack(side=LEFT)

        buttons_font = Font(root=self, family='Arial', size=18)

        self.elements['log_out_button'] = Button(top_frame, text='Log Out',
            bg='#ffffff', activebackground='#f2f2f2', fg='#003399', font=buttons_font,
            activeforeground='#003399', relief=GROOVE, command=self.log_out)
        self.elements['log_out_button'].pack(side=RIGHT, fill=Y)

        self.elements['settings_button'] = Button(top_frame, text='Settings',
            bg='#ffffff', activebackground='#f2f2f2', fg='#003399', font=buttons_font,
            activeforeground='#003399', relief=GROOVE, command=None)
        self.elements['settings_button'].pack(side=RIGHT, fill=Y)

        groups_frame = Frame(self)
        groups_frame.grid(row=1, sticky='NWS')

        listbox_font = Font(root=self, family='Arial', size=14)

        self.elements['groups_listbox'] = Listbox(groups_frame, selectmode=SINGLE, bd=0,
            highlightthickness=0, selectbackground='#333333', font=listbox_font,
            width=15, activestyle='none')
        self.elements['groups_listbox'].bind('<<ListboxSelect>>', self.select_group)
        self.elements['groups_listbox'].pack(side=TOP, expand=False)

        for group in ['Personal'] + [group['name'] for group in self.user_data['groups']]:
            self.elements['groups_listbox'].insert(END, group)

        create_group_button_font = Font(root=self, family='Arial', size=16)

        self.elements['create_group_button'] = Button(groups_frame, text='Create Group',
            bg='#003399', activebackground='#002266', fg='#ffffff', relief=FLAT,
            activeforeground='#ffffff', font=create_group_button_font,
            command=self.create_group)
        self.elements['create_group_button'].pack(side=BOTTOM, expand=True, fill=BOTH)

        self.elements['files_frame'] = Frame(self)
        self.elements['files_frame'].grid(row=1, column=1, sticky='NEWS')

        self.elements['groups_listbox'].select_set(0)
        self.elements['groups_listbox'].event_generate('<<ListboxSelect>>')

    def select_group(self, event=None):
        selected_group_index = self.elements['groups_listbox'].curselection()[0] - 1

        if selected_group_index == -1:
            selected_group = self.user_data
        else:
            selected_group = GroupDataController.get_group_data(
                self.user_data['groups'][selected_group_index]['id'],
                Data().get_token()).payload

        self.elements['files_frame'].grid_forget()
        self.elements['files_frame'].destroy()

        self.elements['files_frame'] = Frame(self)
        self.elements['files_frame'].grid(row=1, column=1, sticky='NEWS')

        self.elements['sidebar_frame'] = Frame(self.elements['files_frame'], bg='#ffffff')
        self.elements['sidebar_frame'].pack(side=RIGHT, expand=False, fill=Y)

        file_data_font = Font(root=self, family='Arial', size=12)

        self.elements['current_file_label'] = Label(self.elements['sidebar_frame'],
            text='Current File', bg='#ffffff', anchor='n', font=file_data_font)
        self.elements['current_file_label'].pack(side=TOP, expand=False, fill=X, padx=35, pady=5)

        files_font = Font(root=self, family='Arial', size=14)

        root_directory = selected_group['files']

        directories = []
        files = []

        for f in root_directory['files']:
            if f['type'] == 'directory':
                directories.append(f)
            else:
                files.append(f)

        for directory in directories:
            Label(self.elements['files_frame'], text=directory['name'], anchor='w',
                font=files_font).pack(side=TOP, expand=False, fill=BOTH, padx=6, pady=(0,3))

        for f in files:
            Label(self.elements['files_frame'], text=f['name'], anchor='w', font=files_font
                ).pack(side=TOP, fill=BOTH, expand=False, padx=6, pady=(0,3))

    def log_out(self):
        Data().set_token('')
        self.parent.set_root_frame('home')

    def create_group(self):
        pass