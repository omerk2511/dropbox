import socket

from common import Message
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
        data = self.socket.recv(BUFFER_SIZE)

        if not data:
            raise Exception('Connection timed out.')

        if len(data) == BUFFER_SIZE:
            while True:
                try:
                    data += self.socket.recv(BUFFER_SIZE)
                except:
                    break
        
        return data