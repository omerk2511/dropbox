from handlers import Server
from models import *

HOST = ''
PORT = 8000

def main():
    Users.initialize()

    server = Server(HOST, PORT)
    server.run()

if __name__ == '__main__':
    main()