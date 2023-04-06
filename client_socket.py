# IGNORE THIS FILE - CURRENTLY NOT IN USE

import socket
import time
import pickle
import pandas
from boardStreamer import __main__ 

def client_program():
    host = socket.gethostname()
    port = 50000 #random unprivileged port
    
    """ Starting a TCP socket. """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    """ Connecting to the server. """    
    client_socket.connect((host, port))

    # Buffer = []

    while __main__:
        client_socket.send(pickle.dumps(__main__.data))   
    
    """ Close the connection from the server. """
    client_socket.close()


if __name__ == '__main__':
    client_program()