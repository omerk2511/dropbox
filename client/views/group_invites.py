from Tkinter import *

from common import Codes
from ..handlers.data import Data
from ..controllers import InviteController

class GroupInvites(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        self.elements = {}
        
        title_frame = Frame(self)
        title_frame.pack(expand=True, fill=BOTH, padx=70, pady=(30, 20))

        self.elements['title'] = Label(title_frame, text='Invites',
            fg='#003399', font=('Arial', 28))
        self.elements['title'].pack(side=TOP)

        self.elements['invites_frame'] = Frame(self)
        self.elements['invites_frame'].pack(side=TOP, padx=120, pady=30,
            expand=False, fill=BOTH)

        self.elements['new_invite_frame'] = Frame(self)
        self.elements['new_invite_frame'].pack(side=TOP, padx=120, pady=30,
            expand=False, fill=BOTH)

        self.elements['invite_frames'] = []

    def initialize(self):
        invites = Data().get_current_group()['invites']
        
        for invite_frame in self.elements['invite_frames']:
            invite_frame.pack_forget()

        self.elements['invite_frames'] = []

        self.elements['invites_frame'].pack_forget()
        self.elements['invites_frame'].pack(side=TOP, padx=120, pady=30,
            expand=False, fill=BOTH)

        self.elements['new_invite_frame'].pack_forget()
        self.elements['new_invite_frame'].pack(side=TOP, padx=120, pady=(10, 30),
            expand=False, fill=BOTH)

        if not invites:
            no_invites_label = Label(self.elements['invites_frame'], bg='gray',
                text='There are no invites to this group.', font=('Arial', 22), anchor='w')
            no_invites_label.pack(side=LEFT, expand=True, fill=X)

            self.elements['invite_frames'].append(no_invites_label)

        for invite in invites:
            invite_frame = Frame(self.elements['invites_frame'], bg='gray')
            invite_frame.pack(side=TOP, expand=False, fill=X, pady=10)

            invite_label = Label(invite_frame, font=('Arial', 18), bg='gray',
                text='%s (%s)' % (invite['user']['username'], invite['user']['full_name']))
            invite_label.pack(side=LEFT, padx=20, pady=10)

            reject_invite_button = Button(invite_frame, text='Revoke',
                font=('Arial', 16), bg='#990000', fg='#ffffff', activebackground='#b30000',
                activeforeground='#ffffff', command=self.generate_revoke_invite(invite['id']))
            reject_invite_button.pack(side=RIGHT, padx=20, pady=10)

            self.elements['invite_frames'].append(invite_frame)

        if 'invite_entry' in self.elements:
            self.elements['invite_entry'].pack_forget()

        self.elements['invite_entry'] = Entry(self.elements['new_invite_frame'],
            font=('Arial', 18))
        self.elements['invite_entry'].pack(side=LEFT, padx=(0, 10), expand=True, fill=BOTH)

        if 'invite_button' in self.elements:
            self.elements['invite_button'].pack_forget()

        self.elements['invite_button'] = Button(self.elements['new_invite_frame'],
            text='Invite', font=('Arial', 18), bg='#003399', activebackground='#002266',
            fg='#ffffff', activeforeground='#ffffff', command=self.invite)
        self.elements['invite_button'].pack(side=LEFT, expand=False, fill=X)

    def invite(self):
        invited_username = self.elements['invite_entry'].get()
        self.elements['invite_entry'].delete(0, END)

        if not invited_username:
            self.parent.display_error('You have to enter a username.')
            return

        server_response = InviteController.invite(Data().get_current_group()['id'],
            invited_username, Data().get_token())

        if server_response.code == Codes.SUCCESS:
            self.parent.display_info('You have succefully created an invitation!')
            self.initialize()
        else:
            self.parent.display_error(server_response.payload['message'])

    def generate_revoke_invite(self, invite_id):
        return lambda: self.revoke_invite(invite_id)

    def revoke_invite(self, invite_id):
        response = InviteController.revoke_invite(invite_id, Data().get_token())

        if response.code == Codes.SUCCESS:
            self.parent.display_info('You have succefully revoked the invite.')
        else:
            self.parent.display_error(response.payload['message'])

        self.initialize()