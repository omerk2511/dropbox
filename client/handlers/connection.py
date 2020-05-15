import socket

from common import Codes, Message
from singleton import Singleton

BUFFER_SIZE = 4096

class Connection(object):
    __metaclass__ = Singleton

    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.socket.connect((host, port))
        except:
            raise Exception('Could not connect to the server.')

        self.socket.settimeout(1)

    def send_recieve(self, message):
        self.socket.send(message.serialize())
        return Message.deserialize(self.recieve_data())

    def recieve_data(self):
        while True:
            try:
                data = self.socket.recv(BUFFER_SIZE)

                if not data:
                    raise Exception('Connection timed out.')

                break
            except socket.timeout:
                pass

        if len(data) == BUFFER_SIZE:
            while True:
                try:
                    data += self.socket.recv(BUFFER_SIZE)
                except:
                    break
        
        return data

    def check_connection(self, gui):
        has_error_ocurred = False

        try:
            response = self.send_recieve(
                Message(
                    Codes.PING,
                    { }
                )
            )

            if response.code != Codes.SUCCESS:
                has_error_ocurred = True
        except Exception as e:
            has_error_ocurred = True

        if has_error_ocurred:
            gui.display_error('Connection timed out.')
            gui.destroy()
            return

        gui.after(1000, lambda: self.check_connection(gui))