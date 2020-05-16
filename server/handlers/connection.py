import socket
from threading import Thread, Event

from common import Codes, Message
from logger import Logger
from ..controllers import *

BUFFER_SIZE = 4096
EVENT_TIMEOUT = 0.00000001

class Connection(Thread):
    def __init__(self, socket, address, server_connections):
        """
        Creates a Connection object
        args: self, socket, address, server_connections
        ret: none
        """

        Thread.__init__(self)

        self.socket = socket
        self.address = address[0] + ':' + str(address[1])

        self.server_connections = server_connections

        self.stop = Event()

        Logger.log_activity(self.address + ' has connected!')

    def run(self):
        """
        Runs the connection
        args: self
        ret: none
        """

        while True:
            should_stop = self.iteration()

            if should_stop:
                break

        self.server_connections.remove(self)

        self.socket.close()
        Logger.log_activity(self.address + ' has disconnected')

    def iteration(self):
        """
        Does a connection iteration (checks for a user request and handles it)
        args: self
        ret: should_stop
        """

        should_stop = self.stop.wait(EVENT_TIMEOUT)

        if should_stop:
            return True

        try:
            data = self.get_data()

            if not data:
                return True

            message = Message.deserialize(data)
            Logger.log_activity(message)

            self.handle_message(message)
        except socket.error:
            pass
        except:
            self.send_bad_request()

        return False

    def handle_message(self, message):
        """
        Handles a user request
        args: self, message
        ret: none
        """

        try:
            controller_func = get_controller_func(message.code)

            if controller_func:
                response = get_controller_func(message.code)(message.payload)
                self.send_message(response)
            else:
                self.send_bad_request()
        except Exception as e:
            Logger.log_error(e)
            self.send_server_error()

    def send_server_error(self):
        """
        Sends a server error message
        args: self
        ret: none
        """

        self.send_message(
            Message(
                Codes.SERVER_ERROR,
                { 'message': 'The server has encountered an internal error.' }
            )
        )

    def send_bad_request(self):
        """
        Sends a bad request message
        args: self
        ret: none
        """

        self.send_message(
            Message(
                Codes.BAD_REQUEST,
                { 'message': 'The server could not understand the request.' }
            )
        )

    def send_message(self, message):
        """
        Sends a message to the user
        args: self, message
        ret: none
        """

        self.socket.send(message.serialize())

    def get_data(self):
        """
        Recieves user data (of any size)
        args: self
        ret: data
        """

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