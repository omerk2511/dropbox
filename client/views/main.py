from Tkinter import *
from tkSimpleDialog import askstring
from tkFileDialog import asksaveasfilename, askopenfilename

from common import Codes
from ..handlers.data import Data
from ..controllers import GroupController, FileController, DirectoryController

class Main(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        self.elements = {}

        self.current_file = None
        self.current_directory = None

    def initialize(self):
        Data().set_user_data()
        self.user_data = Data().get_user_data()

        if self.elements:
            # update the user data based elements

            self.elements['title']['text'] = 'Dropbox - ' + self.user_data['username']

            try:
                selected_group_index = self.elements['groups_listbox'].curselection()[0]
            except:
                selected_group_index = 0

            self.elements['groups_listbox'].delete(0, END)

            for group in ['Personal'] + [group['name'] for group in self.user_data['groups']]:
                self.elements['groups_listbox'].insert(END, group)

            self.elements['groups_listbox'].select_set(selected_group_index)
            self.elements['groups_listbox'].event_generate('<<ListboxSelect>>')

            return
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=200)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)

        top_frame = Frame(self, bg='#003399')
        top_frame.grid(row=0, columnspan=2, sticky='NEW')

        # LOGO

        self.elements['title'] = Label(top_frame, text='Dropbox - ' + self.user_data['username'],
            padx=10, pady=10, fg='#ffffff', bg='#003399', font=('Arial', 22))
        self.elements['title'].pack(side=LEFT)
        self.elements['title'].pack_propagate(False)

        self.elements['log_out_button'] = Button(top_frame, text='Log Out',
            bg='#ffffff', activebackground='#f2f2f2', fg='#003399', font=('Arial', 18),
            activeforeground='#003399', relief=GROOVE, command=self.log_out)
        self.elements['log_out_button'].pack(side=RIGHT, fill=Y)
        self.elements['log_out_button'].pack_propagate(False)

        self.elements['settings_button'] = Button(top_frame, text='Settings',
            bg='#ffffff', activebackground='#f2f2f2', fg='#003399', font=('Arial', 18),
            activeforeground='#003399', relief=GROOVE, command=self.open_settings)
        self.elements['settings_button'].pack(side=RIGHT, fill=Y)
        self.elements['settings_button'].pack_propagate(False)

        self.elements['invites_button'] = Button(top_frame, text='Invites',
            bg='#ffffff', activebackground='#f2f2f2', fg='#003399', font=('Arial', 18),
            activeforeground='#003399', relief=GROOVE, command=self.open_invites)
        self.elements['invites_button'].pack(side=RIGHT, fill=Y)
        self.elements['invites_button'].pack_propagate(False)

        self.elements['leave_button'] = Button(top_frame, text='Leave',
            bg='#ffffff', activebackground='#f2f2f2', fg='#003399', font=('Arial', 18),
            activeforeground='#003399', relief=GROOVE, command=self.leave_group)
        self.elements['leave_button'].pack(side=RIGHT, fill=Y)
        self.elements['leave_button'].pack_propagate(False)

        groups_frame = Frame(self)
        groups_frame.grid(row=1, sticky='NWS')
        groups_frame.grid_propagate(False)

        self.elements['groups_listbox'] = Listbox(groups_frame, selectmode=SINGLE, bd=0,
            highlightthickness=0, selectbackground='#333333', font=('Arial', 14),
            width=25, height=30, activestyle='none')
        self.elements['groups_listbox'].bind('<<ListboxSelect>>', self.select_group)
        self.elements['groups_listbox'].pack(side=TOP, expand=False)

        for group in ['Personal'] + [group['name'] for group in self.user_data['groups']]:
            self.elements['groups_listbox'].insert(END, group)

        self.elements['create_group_button'] = Button(groups_frame, text='Create Group',
            bg='#003399', activebackground='#002266', fg='#ffffff', relief=FLAT,
            activeforeground='#ffffff', font=('Arial', 16),
            command=self.create_group)
        self.elements['create_group_button'].pack(side=BOTTOM, expand=True, fill=BOTH)

        self.elements['files_frame'] = Frame(self)
        self.elements['files_frame'].grid(row=1, column=1, sticky='NEWS')

        self.elements['groups_listbox'].select_set(0)
        self.elements['groups_listbox'].event_generate('<<ListboxSelect>>')

    def select_group(self, event=None):
        self.elements['settings_button'].pack_forget()
        self.elements['invites_button'].pack_forget()
        self.elements['leave_button'].pack_forget()

        selected_group_index = self.elements['groups_listbox'].curselection()[0] - 1

        if selected_group_index == -1:
            Data().set_user_data()
            self.user_data = Data().get_user_data()

            self.selected_group = self.user_data

            self.elements['settings_button'].pack(side=RIGHT, fill=Y)
            self.elements['invites_button'].pack(side=RIGHT, fill=Y)
        else:
            self.selected_group = GroupController.get_group_data(
                self.user_data['groups'][selected_group_index]['id'],
                Data().get_token()).payload

            if self.selected_group['owner']['id'] == self.user_data['id']:
                self.elements['settings_button'].pack(side=RIGHT, fill=Y)
                self.elements['invites_button'].pack(side=RIGHT, fill=Y)
            else:
                self.elements['leave_button'].pack(side=RIGHT, fill=Y)

        self.elements['files_frame'].grid_forget()
        self.elements['files_frame'].destroy()

        self.elements['files_frame'] = Frame(self)
        self.elements['files_frame'].grid(row=1, column=1, sticky='NEWS')

        self.elements['current_file_frame'] = Frame(self.elements['files_frame'],
            width=250, bg='#ffffff')
        self.elements['current_file_frame'].pack(side=RIGHT, expand=False, fill=Y)
        self.elements['current_file_frame'].pack_propagate(False)

        self.elements['current_file_name_label'] = Label(self.elements['current_file_frame'],
            text='', bg='#ffffff', anchor='n', font=('Arial', 14))
        self.elements['current_file_name_label'].pack(side=TOP, expand=False, fill=X, padx=35, pady=5)

        self.elements['current_file_type_label'] = Label(self.elements['current_file_frame'],
            text='', bg='#ffffff', anchor='n', font=('Arial', 12))
        self.elements['current_file_type_label'].pack(side=TOP, expand=False, fill=X, padx=10, pady=1)

        self.elements['current_file_owner_label'] = Label(self.elements['current_file_frame'],
            text='', bg='#ffffff', anchor='n', font=('Arial', 12))
        self.elements['current_file_owner_label'].pack(side=TOP, expand=False, fill=X, padx=10, pady=1)

        self.elements['download_file_button'] = Button(self.elements['current_file_frame'],
            text='Download File', font=('Arial', 14), command=self.download_file)

        self.elements['delete_button'] = Button(self.elements['current_file_frame'],
            text='Delete', font=('Arial', 14), command=self.delete_file)

        self.elements['file_buttons_frame'] = Frame(self.elements['files_frame'])
        self.elements['file_buttons_frame'].pack(side=BOTTOM, expand=False, fill=X)

        self.elements['create_file_button'] = Button(self.elements['file_buttons_frame'],
            text='Upload File', font=('Arial', 16), command=self.create_file, bg='#ffffff',
            activebackground='#f2f2f2', fg='#003399', activeforeground='#003399')
        self.elements['create_file_button'].pack(side=LEFT, expand=True, fill=X)

        self.elements['create_directory_button'] = Button(self.elements['file_buttons_frame'],
            text='Create Directory', font=('Arial', 16), command=self.create_directory,
            bg='#ffffff', activebackground='#f2f2f2', fg='#003399', activeforeground='#003399')
        self.elements['create_directory_button'].pack(side=RIGHT, expand=True, fill=X)

        root_directory = self.selected_group['files']
        self.shown_directory = root_directory['id']

        directories = []
        files = []

        for f in root_directory['files']:
            if f['type'] == 'directory':
                directories.append(f)
            else:
                files.append(f)

        for directory in directories:
            directory_label = Label(self.elements['files_frame'], text=directory['name'],
                anchor='w', font=('Arial', 14))
            directory_label.pack(side=TOP, expand=False, fill=BOTH, padx=6, pady=(3, 1))

            directory_label.bind('<Button-1>',
                self.generate_select_file(self.selected_group, directory_id=directory['id']))
            directory_label.bind('<Double-Button-1>',
                self.generate_select_directory(directory_id=directory['id']))

            self.elements['directory_label_' + str(directory['id'])] = directory_label

        for f in files:
            file_label = Label(self.elements['files_frame'], text=f['name'],
                anchor='w', font=('Arial', 14))
            file_label.pack(side=TOP, fill=BOTH, expand=False, padx=6, pady=(3, 1))

            file_label.bind('<Button-1>',
                self.generate_select_file(self.selected_group, file_id=f['id']))
            file_label.bind('<Double-Button-1>', self.download_file)

            self.elements['file_label_' + str(f['id'])] = file_label

        self.currently_selected_file = None

    def select_file(self, group, file_id=None, directory_id=None):
        if self.currently_selected_file:
            self.currently_selected_file['bg'] = 'SystemButtonFace'

        self.elements['delete_button'].pack_forget()

        if file_id:
            self.current_file = file_id

            self.currently_selected_file = self.elements['file_label_' + str(file_id)]
            file_info = Data().get_file_info(group, file_id)

            self.elements['current_file_name_label']['text'] = (file_info['name'] if
                len(file_info['name']) < 14 else file_info['name'][:11] + '...')
            self.elements['current_file_type_label']['text'] = 'Type: ' + file_info['type']
            self.elements['current_file_owner_label']['text'] = 'Owner: ' + file_info['owner']['full_name']
            
            self.elements['download_file_button'].pack(side=TOP, expand=False, fill=X, padx=10, pady=(20, 0))

            if file_info['owner']['id'] == Data().get_user_data()['id'] or (
                'owner' in self.selected_group and 
                self.selected_group['owner']['id'] == Data().get_user_data()['id']):
                self.elements['delete_button'].pack(side=TOP, expand=False, fill=X, padx=10, pady=(20, 0))

        if directory_id:
            self.currently_selected_file = self.elements['directory_label_' + str(directory_id)]

            if directory_id == -1:
                self.elements['current_file_name_label']['text'] = ''
                self.elements['current_file_type_label']['text'] = ''
                self.elements['current_file_owner_label']['text'] = ''

                self.elements['download_file_button'].pack_forget()
                self.elements['delete_button'].pack_forget()
            else:
                self.current_file = None
                self.current_directory = directory_id

                directory_info = Data().get_directory_info(group, directory_id)

                self.elements['current_file_name_label']['text'] = (directory_info['name']
                    if len(directory_info['name']) < 14 else directory_info['name'][:11] + '...')
                self.elements['current_file_type_label']['text'] = 'Type: ' + directory_info['type']
                self.elements['current_file_owner_label']['text'] = 'Owner: ' + directory_info['owner']['full_name']

                self.elements['download_file_button'].pack_forget()

                if directory_info['owner']['id'] == Data().get_user_data()['id'] or (
                    'owner' in self.selected_group and 
                    self.selected_group['owner']['id'] == Data().get_user_data()['id']):
                    self.elements['delete_button'].pack(side=TOP, expand=False, fill=X, padx=10, pady=(20, 0))

        self.currently_selected_file['bg'] = 'gray'

    def generate_select_file(self, group, file_id=None, directory_id=None):
        return lambda e: self.select_file(group, file_id, directory_id)

    def select_directory(self, directory_id):
        self.elements['files_frame'].grid_forget()
        self.elements['files_frame'].destroy()

        self.elements['files_frame'] = Frame(self)
        self.elements['files_frame'].grid(row=1, column=1, sticky='NEWS')

        self.elements['current_file_frame'] = Frame(self.elements['files_frame'],
            width=250, bg='#ffffff')
        self.elements['current_file_frame'].pack(side=RIGHT, expand=False, fill=Y)
        self.elements['current_file_frame'].pack_propagate(False)

        self.elements['current_file_name_label'] = Label(self.elements['current_file_frame'],
            text='', bg='#ffffff', anchor='n', font=('Arial', 14))
        self.elements['current_file_name_label'].pack(side=TOP, expand=False, fill=X, padx=35, pady=5)
        
        self.elements['current_file_type_label'] = Label(self.elements['current_file_frame'],
            text='', bg='#ffffff', anchor='n', font=('Arial', 12))
        self.elements['current_file_type_label'].pack(side=TOP, expand=False, fill=X, padx=10, pady=1)

        self.elements['current_file_owner_label'] = Label(self.elements['current_file_frame'],
            text='', bg='#ffffff', anchor='n', font=('Arial', 12))
        self.elements['current_file_owner_label'].pack(side=TOP, expand=False, fill=X, padx=10, pady=1)

        self.elements['download_file_button'] = Button(self.elements['current_file_frame'],
            text='Download File', font=('Arial', 14), command=self.download_file)

        self.elements['delete_button'] = Button(self.elements['current_file_frame'],
            text='Delete', font=('Arial', 14), command=self.delete_file)

        self.elements['file_buttons_frame'] = Frame(self.elements['files_frame'])
        self.elements['file_buttons_frame'].pack(side=BOTTOM, expand=False, fill=X)

        self.elements['create_file_button'] = Button(self.elements['file_buttons_frame'],
            text='Upload File', font=('Arial', 16), command=self.create_file, bg='#ffffff',
            activebackground='#f2f2f2', fg='#003399', activeforeground='#003399')
        self.elements['create_file_button'].pack(side=LEFT, expand=True, fill=X)

        self.elements['create_directory_button'] = Button(self.elements['file_buttons_frame'],
            text='Create Directory', font=('Arial', 16), command=self.create_directory,
            bg='#ffffff', activebackground='#f2f2f2', fg='#003399', activeforeground='#003399')
        self.elements['create_directory_button'].pack(side=RIGHT, expand=True, fill=X)

        root_directory = None
        
        directories = self.selected_group['files']['files']
        
        if directory_id == self.selected_group['files']['id']:
            root_directory = self.selected_group['files']

        if directory_id == -1:
            if self.current_directory in [f['id'] for f
                in directories if f['type'] == 'directory']:
                root_directory = self.selected_group['files']

            while directories and not root_directory:            
                if directories[0]['type'] == 'directory':
                    if self.current_directory in [f['id'] for
                        f in directories[0]['files'] if f['type'] == 'directory']:
                        root_directory = directories[0]

                    directories += directories[0]['files']
                
                directories = directories[1:]
        else:
            while directories and not root_directory:            
                if directories[0]['type'] == 'directory':
                    if directories[0]['id'] == directory_id:
                        root_directory = directories[0]

                    directories += directories[0]['files']
                
                directories = directories[1:]

        self.shown_directory = root_directory['id']

        if root_directory == self.selected_group['files']:
            directories = []
        else:
            directories = [
                { 'name': '../', 'id': -1 }
            ]

        files = []

        for f in root_directory['files']:
            if f['type'] == 'directory':
                directories.append(f)
            else:
                files.append(f)

        for directory in directories:
            directory_label = Label(self.elements['files_frame'], text=directory['name'],
                anchor='w', font=('Arial', 14))
            directory_label.pack(side=TOP, expand=False, fill=BOTH, padx=6, pady=(3, 1))

            directory_label.bind('<Button-1>',
                self.generate_select_file(self.selected_group, directory_id=directory['id']))
            directory_label.bind('<Double-Button-1>',
                self.generate_select_directory(directory_id=directory['id']))

            self.elements['directory_label_' + str(directory['id'])] = directory_label

        for f in files:
            file_label = Label(self.elements['files_frame'], text=f['name'],
                anchor='w', font=('Arial', 14))
            file_label.pack(side=TOP, fill=BOTH, expand=False, padx=6, pady=(3, 1))

            file_label.bind('<Button-1>',
                self.generate_select_file(self.selected_group, file_id=f['id']))
            file_label.bind('<Double-Button-1>', self.download_file)

            self.elements['file_label_' + str(f['id'])] = file_label

        self.currently_selected_file = None
        self.current_directory = root_directory['id']

    def generate_select_directory(self, directory_id):
        return lambda e: self.select_directory(directory_id)

    def download_file(self, event=None):
        if self.current_file:
            file_extension = None

            splitted_file = self.elements['file_label_' +
                str(self.current_file)]['text'].split('.')

            if len(splitted_file) > 1:
                file_extension = splitted_file[-1]

            if file_extension:
                file_name = asksaveasfilename(initialdir='/', title='Select File',
                    filetypes=[('Original File Type', '.' + file_extension)])
            else:
                file_name = asksaveasfilename(initialdir='/', title='Select File')

            if file_name:
                if not file_name.endswith('.' + file_extension):
                    file_name += '.' + file_extension

                content = FileController.get_file_content(
                    self.current_file, Data().get_token())

                with open(file_name, 'wb') as f:
                    f.write(content)

                self.parent.display_info('File downloaded successfully!')

    def delete_file(self):
        if self.current_file:
            file_directory = self.shown_directory

            response = FileController.delete_file(self.current_file,
                Data().get_token())

            if response.code == Codes.SUCCESS:
                self.parent.display_info('The file was deleted successfully!')

                self.select_group()
                self.select_directory(file_directory)
            else:
                self.parent.display_error(response.payload['message'])
        elif self.current_directory:
            print 'delete directory', self.current_directory

    def create_file(self):
        file_name = askopenfilename(initialdir='/', title='Select File')

        if file_name:
            actual_name = file_name.split('/')[-1]
            file_directory = self.shown_directory

            with open(file_name, 'rb') as f:
                response = FileController.create_file(actual_name, file_directory,
                    f.read(), Data().get_token())

                if response.code == Codes.SUCCESS:
                    self.parent.display_info('The file was successfully uploaded!')

                    self.select_group()
                    self.select_directory(file_directory)
                else:
                    self.parent.display_error(response.payload['message'])

    def create_directory(self):
        directory_name = askstring('Required Input',
            'Enter a name for the directory:', parent=self)

        if directory_name:
            if not directory_name.endswith('/'):
                directory_name += '/'

            parent = self.shown_directory

            selected_group_index = self.elements['groups_listbox'].curselection()[0] - 1

            if selected_group_index == -1:
                response = DirectoryController.create_directory(directory_name,
                    parent, Data().get_token())
            else:
                group_id = self.user_data['groups'][selected_group_index]['id']

                response = DirectoryController.create_directory(directory_name,
                    parent, Data().get_token(), group_id)

            if response.code == Codes.SUCCESS:
                self.parent.display_info('Created a directory successfully!')

                self.select_group()
                self.select_directory(parent)
            else:
                self.parent.display_error(response.payload['message'])
        else:
            self.parent.display_error('You have to give the directory a name!')

    def leave_group(self):
        selected_group_index = self.elements['groups_listbox'].curselection()[0] - 1

        if selected_group_index != -1:
            current_group = self.user_data['groups'][selected_group_index]['id']
            response = GroupController.leave_group(current_group, Data().get_token())

            if response.code == Codes.SUCCESS:
                self.parent.display_info('You have successfully left the group!')

                self.elements['groups_listbox'].delete(selected_group_index + 1)

                self.elements['groups_listbox'].select_set(0)
                self.elements['groups_listbox'].event_generate('<<ListboxSelect>>')
            else:
                self.parent.display_error(response.payload['message'])

    def log_out(self):
        Data().set_token('')
        self.parent.set_root_frame('home')

    def open_settings(self):
        selected_group_index = self.elements['groups_listbox'].curselection()[0] - 1

        if selected_group_index == -1:
            self.parent.show_frame('user_settings')
        else:
            Data().set_current_group(self.user_data['groups'][selected_group_index]['id'])
            self.parent.show_frame('group_settings')

    def open_invites(self):
        selected_group_index = self.elements['groups_listbox'].curselection()[0] - 1

        if selected_group_index == -1:
            self.parent.show_frame('user_invites')
        else:
            Data().set_current_group(self.user_data['groups'][selected_group_index]['id'])
            self.parent.show_frame('group_invites')

    def create_group(self):
        group_name = askstring('Required Input',
            'Enter a name for the group:', parent=self)

        if group_name:
            try:
                response = GroupController.create_group(group_name, Data().get_token())
            except:
                self.parent.display_error('Connection timed out.')
                self.parent.quit()

            if response.code == Codes.SUCCESS:
                self.parent.display_info('Created a group successfully.')
                self.initialize()
            else:
                self.parent.display_error(response.payload['message'])
        else:
            self.parent.display_error('You have to give the group a name!')