import socket

from connection import Connection
from database import database

class Server(object):
    def __init__(self, host, port):
        """
        Creates a Server object
        args: self, host, port
        ret: none
        """

        print '[*] Hello there!'

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.settimeout(1)

        self.socket.bind((host, port))
        self.socket.listen(5)

        self.connections = []

    def run(self):
        """
        Runs the server main loop
        args: self
        ret: none
        """

        try:
            while True:
                try:
                    client_socket, client_address = self.socket.accept()
                    
                    connection = Connection(client_socket, client_address, self.connections)
                    connection.start()

                    self.connections.append(connection)
                except socket.timeout:
                    continue
        except KeyboardInterrupt:
            for connection in self.connections:
                connection.stop.set()
                connection.join()

            self.socket.close()

            print '[*] Bye bye!'