from threading import Thread

class Connection(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)

        self.socket = socket
        self.address = address

        self.should_run = True

        print '[+]', self.address[0] + ':' + str(self.address[1]), 'has connected'

    def run(self):
        while self.should_run:
            pass
            # actual client handling function
        
        # should clean itself from Server connections list

        self.socket.close()
        print '[-]', self.address[0] + ':' + str(self.address[1]), 'has disconnected'

    def stop(self):
        self.should_run = False