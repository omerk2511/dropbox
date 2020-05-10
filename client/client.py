from gui import GUI
from handlers import Connection, Client

HOST = ''
PORT = 8000

def main():
    gui = GUI()
    connection = Connection(HOST, PORT)

    client = Client(gui, connection)
    client.run()

if __name__ == '__main__':
    main()