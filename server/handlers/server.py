import socket

class Server(object):
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.settimeout(1)

        self.socket.bind((host, port))
        self.socket.listen(5)

    def run(self):
        try:
            while True:
                try:
                    client_socket, client_address = self.socket.accept()

                    # some dummy socket handling code (should by done by a handler)
                    print '[+]', client_address[0] + ':' + str(client_address[1]), 'has connected'

                    client_socket.send('LOL!')

                    client_socket.close()
                    print '[-]', client_address[0] + ':' + str(client_address[1]), 'has disconnected'

                    # should actually create a connection object which derives from Thread
                except socket.timeout:
                    continue
        except KeyboardInterrupt:
            print '[*] Bye bye!'

            self.socket.close()
            # should close all connections