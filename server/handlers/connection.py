from threading import Thread, Event

class Connection(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)

        self.socket = socket
        self.address = address[0] + ':' + str(address[1])

        self.stop = Event()

        print '[+]', self.address, 'has connected'

    def run(self):
        while True:
            should_stop = self.stop.wait(0.0001) # TODO: move into a constant

            if should_stop:
                break

            # actual client handling function
        
        # should clean itself from Server connections list

        self.socket.close()
        print '[-]', self.address, 'has disconnected'