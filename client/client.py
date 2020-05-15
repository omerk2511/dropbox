import sys

from handlers import GUI, Data, Connection

HOST = 'localhost'
PORT = 8000

def close():
    connection.socket.close()
    gui.destroy()

if __name__ == '__main__':
    gui = GUI()
    gui.protocol('WM_DELETE_WINDOW', close)

    data = Data()
    
    try:
        connection = Connection(HOST, PORT)
    except:
        gui.display_error('Could not connect to the server.')
        sys.exit(1)

    gui.initialize_frames()
    gui.mainloop()