from Tkinter import *

from common import Codes
from ..handlers.data import Data
from ..controllers import InviteController

class UserInvites(Frame):
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

        self.elements['invite_frames'] = []

    def initialize(self):
        invites = Data().get_user_data()['invites']
        
        for invite_frame in self.elements['invite_frames']:
            invite_frame.pack_forget()

        self.elements['invite_frames'] = []

        self.elements['invites_frame'].pack_forget()
        self.elements['invites_frame'].pack(side=TOP, padx=120, pady=30,
            expand=False, fill=BOTH)

        for invite in invites:
            invite_frame = Frame(self.elements['invites_frame'], bg='gray')
            invite_frame.pack(side=TOP, expand=False, fill=X, pady=10)

            invite_label = Label(invite_frame, font=('Arial', 18), bg='gray',
                text='%s (%s)' % (invite['group']['name'], invite['group']['owner']['full_name']))
            invite_label.pack(side=LEFT, padx=20, pady=10)

            accept_invite_button = Button(invite_frame, text='Accept',
                font=('Arial', 16), bg='#004d00', fg='#ffffff', activebackground='#006600',
                activeforeground='#ffffff', command=self.generate_accept_invite(invite['id']))
            accept_invite_button.pack(side=RIGHT, padx=20, pady=10)

            reject_invite_button = Button(invite_frame, text='Reject',
                font=('Arial', 16), bg='#990000', fg='#ffffff', activebackground='#b30000',
                activeforeground='#ffffff', command=self.generate_reject_invite(invite['id']))
            reject_invite_button.pack(side=RIGHT, pady=10)

            self.elements['invite_frames'].append(invite_frame)

    def generate_accept_invite(self, invite_id):
        return lambda: self.accept_invite(invite_id)

    def generate_reject_invite(self, invite_id):
        return lambda: self.reject_invite(invite_id)

    def accept_invite(self, invite_id):
        response = InviteController.accept_invite(invite_id, Data().get_token())

        if response.code == Codes.SUCCESS:
            self.parent.display_info('You have succefully joined the group!')
        else:
            self.parent.display_error(response.payload['message'])

        Data().set_user_data()
        self.initialize()

    def reject_invite(self, invite_id):
        response = InviteController.reject_invite(invite_id, Data().get_token())

        if response.code == Codes.SUCCESS:
            self.parent.display_info('You have succefully rejected the invite.')
        else:
            self.parent.display_error(response.payload['message'])

        Data().set_user_data()
        self.initialize()