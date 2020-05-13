from Tkinter import *
from tkFont import *
from tkFileDialog import asksaveasfilename

from common import Codes
from ..handlers.data import Data
from ..controllers import GroupController, FileController

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
            self.selected_group = self.user_data
        else:
            self.selected_group = GroupController.get_group_data(
                self.user_data['groups'][selected_group_index]['id'],
                Data().get_token()).payload

        self.elements['files_frame'].grid_forget()
        self.elements['files_frame'].destroy()

        self.elements['files_frame'] = Frame(self)
        self.elements['files_frame'].grid(row=1, column=1, sticky='NEWS')

        self.elements['current_file_frame'] = Frame(self.elements['files_frame'], bg='#ffffff')
        self.elements['current_file_frame'].pack(side=RIGHT, expand=False, fill=Y)

        file_name_font = Font(root=self, family='Arial', size=14)

        self.elements['current_file_name_label'] = Label(self.elements['current_file_frame'],
            text='', bg='#ffffff', anchor='n', font=file_name_font)
        self.elements['current_file_name_label'].pack(side=TOP, expand=False, fill=X, padx=35, pady=5)
        
        file_data_font = Font(root=self, family='Arial', size=12)

        self.elements['current_file_type_label'] = Label(self.elements['current_file_frame'],
            text='', bg='#ffffff', anchor='n', font=file_data_font)
        self.elements['current_file_type_label'].pack(side=TOP, expand=False, fill=X, padx=10, pady=1)

        self.elements['current_file_owner_label'] = Label(self.elements['current_file_frame'],
            text='', bg='#ffffff', anchor='n', font=file_data_font)
        self.elements['current_file_owner_label'].pack(side=TOP, expand=False, fill=X, padx=10, pady=1)

        self.elements['download_file_button'] = Button(self.elements['current_file_frame'],
            text='Download File', font=file_name_font, command=self.download_file)

        self.elements['delete_button'] = Button(self.elements['current_file_frame'],
            text='Delete', font=file_name_font, command=self.delete_file)

        files_font = Font(root=self, family='Arial', size=14)

        root_directory = self.selected_group['files']

        directories = []
        files = []

        for f in root_directory['files']:
            if f['type'] == 'directory':
                directories.append(f)
            else:
                files.append(f)

        for directory in directories:
            directory_label = Label(self.elements['files_frame'], text=directory['name'],
                anchor='w', font=files_font)
            directory_label.pack(side=TOP, expand=False, fill=BOTH, padx=6, pady=(3, 1))

            directory_label.bind('<Button-1>',
                self.generate_select_file(self.selected_group, directory_id=directory['id']))
            directory_label.bind('<Double-Button-1>',
                self.generate_select_directory(self.selected_group, directory_id=directory['id']))

            self.elements['directory_label_' + str(directory['id'])] = directory_label

        for f in files:
            file_label = Label(self.elements['files_frame'], text=f['name'],
                anchor='w', font=files_font)
            file_label.pack(side=TOP, fill=BOTH, expand=False, padx=6, pady=(3, 1))

            file_label.bind('<Button-1>',
                self.generate_select_file(self.selected_group, file_id=f['id']))

            self.elements['file_label_' + str(f['id'])] = file_label

        self.currently_selected_file = None

    def select_file(self, group, file_id=None, directory_id=None):
        if self.currently_selected_file:
            self.currently_selected_file['bg'] = 'SystemButtonFace'

        self.elements['delete_button'].pack_forget()

        self.current_file = None
        self.current_directory = None

        if file_id:
            self.current_file = file_id

            self.currently_selected_file = self.elements['file_label_' + str(file_id)]
            file_info = Data().get_file_info(group, file_id)

            self.elements['current_file_name_label']['text'] = file_info['name']
            self.elements['current_file_type_label']['text'] = 'Type: ' + file_info['type']
            self.elements['current_file_owner_label']['text'] = 'Owner: ' + file_info['owner']['full_name']
            
            self.elements['download_file_button'].pack(side=TOP, expand=False, fill=X, padx=10, pady=(20, 0))

            if file_info['owner']['id'] == Data().get_user_data()['id']:
                self.elements['delete_button'].pack(side=TOP, expand=False, fill=X, padx=10, pady=(20, 0))

        if directory_id:
            self.current_directory = directory_id

            self.currently_selected_file = self.elements['directory_label_' + str(directory_id)]
            directory_info = Data().get_directory_info(group, directory_id)

            self.elements['current_file_name_label']['text'] = directory_info['name']
            self.elements['current_file_type_label']['text'] = 'Type: ' + directory_info['type']
            self.elements['current_file_owner_label']['text'] = 'Owner: ' + directory_info['owner']['full_name']

            self.elements['download_file_button'].pack_forget()

            if directory_info['owner']['id'] == Data().get_user_data()['id']:
                self.elements['delete_button'].pack(side=TOP, expand=False, fill=X, padx=10, pady=(20, 0))

        self.currently_selected_file['bg'] = 'gray'

    def generate_select_file(self, group, file_id=None, directory_id=None):
        return lambda e: self.select_file(group, file_id, directory_id)

    def select_directory(self, group, directory_id):
        self.elements['files_frame'].grid_forget()
        self.elements['files_frame'].destroy()

        self.elements['files_frame'] = Frame(self)
        self.elements['files_frame'].grid(row=1, column=1, sticky='NEWS')

        self.elements['current_file_frame'] = Frame(self.elements['files_frame'], bg='#ffffff')
        self.elements['current_file_frame'].pack(side=RIGHT, expand=False, fill=Y)

        file_name_font = Font(root=self, family='Arial', size=14)

        self.elements['current_file_name_label'] = Label(self.elements['current_file_frame'],
            text='', bg='#ffffff', anchor='n', font=file_name_font)
        self.elements['current_file_name_label'].pack(side=TOP, expand=False, fill=X, padx=35, pady=5)
        
        file_data_font = Font(root=self, family='Arial', size=12)

        self.elements['current_file_type_label'] = Label(self.elements['current_file_frame'],
            text='', bg='#ffffff', anchor='n', font=file_data_font)
        self.elements['current_file_type_label'].pack(side=TOP, expand=False, fill=X, padx=10, pady=1)

        self.elements['current_file_owner_label'] = Label(self.elements['current_file_frame'],
            text='', bg='#ffffff', anchor='n', font=file_data_font)
        self.elements['current_file_owner_label'].pack(side=TOP, expand=False, fill=X, padx=10, pady=1)

        self.elements['download_file_button'] = Button(self.elements['current_file_frame'],
            text='Download File', font=file_name_font, command=self.download_file)

        self.elements['delete_button'] = Button(self.elements['current_file_frame'],
            text='Delete', font=file_name_font, command=self.delete_file)

        files_font = Font(root=self, family='Arial', size=14)

        root_directory = None
        
        directories = self.selected_group['files']['files']

        while directories and not root_directory:            
            if directories[0]['type'] == 'directory':
                if directories[0]['id'] == directory_id:
                    root_directory = directories[0]

                directories += directories[0]['files']
            
            directories = directories[1:]

        directories = []
        files = []

        for f in root_directory['files']:
            if f['type'] == 'directory':
                directories.append(f)
            else:
                files.append(f)

        for directory in directories:
            directory_label = Label(self.elements['files_frame'], text=directory['name'],
                anchor='w', font=files_font)
            directory_label.pack(side=TOP, expand=False, fill=BOTH, padx=6, pady=(3, 1))

            directory_label.bind('<Button-1>',
                self.generate_select_file(self.selected_group, directory_id=directory['id']))
            directory_label.bind('<Double-Button-1>',
                self.generate_select_directory(self.selected_group, directory_id=directory['id']))

            self.elements['directory_label_' + str(directory['id'])] = directory_label

        for f in files:
            file_label = Label(self.elements['files_frame'], text=f['name'],
                anchor='w', font=files_font)
            file_label.pack(side=TOP, fill=BOTH, expand=False, padx=6, pady=(3, 1))

            file_label.bind('<Button-1>',
                self.generate_select_file(self.selected_group, file_id=f['id']))

            self.elements['file_label_' + str(f['id'])] = file_label

        self.currently_selected_file = None

    def generate_select_directory(self, group, directory_id):
        return lambda e: self.select_directory(group, directory_id)

    def download_file(self):
        if self.current_file:
            file_extension = FileController.get_file_extension(
                self.current_file, Data().get_token())

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
            response = FileController.delete_file(self.current_file,
                Data().get_token())

            if response.code == Codes.SUCCESS:
                self.parent.display_info('The file was deleted successfully!')
                self.select_group()
            else:
                self.parent.display_error(response.payload['message'])

        if self.current_directory:
            print 'delete directory', self.current_directory

    def log_out(self):
        Data().set_token('')
        self.parent.set_root_frame('home')

    def create_group(self):
        self.parent.show_frame('create_group')