import socket
import pickle
import boardStreamer
from boardStreamer import __main__


def server_program():
    host = socket.gethostname()
    port = 65400 #random unprivileged port

    """ Starting a TCP socket. """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    """ Bind the IP and PORT to the server. """
    server_socket.bind((host, port))
    
    """ Start Server Listening"""
    server_socket.listen()

    """ Server accepts connection from client"""
    conn, address = server_socket.accept()
    print("Connection from: " + str(address))

    buffer = []
    i = 0

    while True:

        data = conn.recv(1024)
        buffer.append(pickle.loads(data))
        print(buffer[i])
        i = i + 1
    
    conn.close()
    print(f"[DISCONNECTED] {address} disconnected.")


if __name__ == '__main__':
    server_program()

