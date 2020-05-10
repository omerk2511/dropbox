class Connection(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port

        # create socket