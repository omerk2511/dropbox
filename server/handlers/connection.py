import socket

from threading import Thread, Event

from common import Codes, Message
from ..controllers import *

# TODO: find an appropriate place for these constants
BUFFER_SIZE = 4096
EVENT_TIMEOUT = 0.00000001

class Connection(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)

        self.socket = socket
        self.address = address[0] + ':' + str(address[1])

        self.stop = Event()

        print '[+]', self.address, 'has connected'

    def run(self):
        while True:
            should_stop = self.iteration()

            if should_stop:
                break

        # should clean itself from Server connections list

        self.socket.close()
        print '[-]', self.address, 'has disconnected'

    def iteration(self):
        should_stop = self.stop.wait(EVENT_TIMEOUT)

        if should_stop:
            return True

        try:
            data = self.get_data()

            if not data:
                return True

            message = Message.deserialize(data)
            print '[*]', message

            self.handle_message(message)
        except socket.error:
            pass
        except:
            self.send_bad_request()

        return False

    def handle_message(self, message):
        try:
            response = get_controller_func(message.code)(message.payload)
            self.send_message(response)
        except:
            self.send_bad_request(message)

    def send_bad_request(self):
        self.send_message(
            Message(
                Codes.BAD_REQUEST,
                { 'message': 'The server could not understand the request.' }
            )
        )

    def send_message(self, message):
        self.socket.send(message.serialize())

    def get_data(self):
        data = self.socket.recv(BUFFER_SIZE)

        if not data:
            return None

        if len(data) == BUFFER_SIZE:
            while True:
                try:
                    data += self.socket.recv(BUFFER_SIZE)
                except:
                    break
        
        return data