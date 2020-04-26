from threading import Thread, Event

from common.message import Message

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
            should_stop = self.stop.wait(EVENT_TIMEOUT)

            if should_stop:
                break

            try:
                data = self.socket.recv(BUFFER_SIZE)

                if not data:
                    break

                if len(data) == BUFFER_SIZE:
                    while True:
                        try:
                            data += self.socket.recv(BUFFER_SIZE)
                        except:
                            break
            except:
                continue

            data = data.strip()
            
            try:
                message = Message.deserialize(data)
                print '[*]', message
            except:
                pass # send a format error

        # should clean itself from Server connections list

        self.socket.close()
        print '[-]', self.address, 'has disconnected'