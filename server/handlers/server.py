import socket

from connection import Connection

class Server(object):
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.settimeout(1)

        self.socket.bind((host, port))
        self.socket.listen(5)

        self.connections = []

    def run(self):
        try:
            while True:
                try:
                    client_socket, client_address = self.socket.accept()
                    
                    connection = Connection(client_socket, client_address)
                    connection.start()

                    self.connections.append(connection)
                except socket.timeout:
                    continue
        except KeyboardInterrupt:
            self.socket.close()

            for connection in self.connections:
                connection.stop()
                connection.join()

            print '[*] Bye bye!'