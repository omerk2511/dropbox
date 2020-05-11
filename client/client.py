from handlers import GUI, Data, Connection

HOST = 'localhost'
PORT = 8000

def main():
    gui = GUI()
    data = Data()
    
    try:
        connection = Connection(HOST, PORT)
    except:
        gui.display_error('Could not connect to the server.')
        return

    gui.initialize_frames()
    gui.mainloop()

if __name__ == '__main__':
    main()