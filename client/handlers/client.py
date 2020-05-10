class Client(object):
    def __init__(self, gui, connection):
        self.gui = gui
        self.connection = connection

        # set everything up

    def run(self):
        self.gui.mainloop()
        #run main loop