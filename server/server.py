from handlers import Server
from models import initialize_models

HOST = ''
PORT = 8000

def main():
    """
    The main server function
    args: none
    ret: none
    """

    initialize_models()

    server = Server(HOST, PORT)
    server.run()

if __name__ == '__main__':
    main()