from handlers import GUI, Connection

HOST = 'localhost'
PORT = 8000

def main():
    gui = GUI()
    
    try:
        connection = Connection(HOST, PORT)
    except:
        gui.display_error('Could not connect to the server.')
        return

    gui.mainloop()

if __name__ == '__main__':
    main()