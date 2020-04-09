from handlers.server import Server

HOST = ''
PORT = 8000

def main():
    server = Server(HOST, PORT)
    server.run()

if __name__ == '__main__':
    main()