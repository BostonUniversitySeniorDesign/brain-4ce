import socket
import pickle


def server_program():
    host = socket.gethostname()
    port = 65400 #random unprivileged port

    """ Starting a TCP socket. """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    """ Bind the IP and PORT to the server. """
    server_socket.bind((host, port))
    print("[STARTING] Server is starting.")
    
    """ Start Server Listening"""
    server_socket.listen()
    print("[LISTENING] Server is listening.")

    """ Server accepts connection from client"""
    conn, address = server_socket.accept()
    print("Connection from: " + str(address))

    data = conn.recv(1024).decode()
    buffer = []
    i = 0

    while True:

        data = conn.recv(10000)
        buffer.append(pickle.loads(data))
        print(buffer[i])
        i = i + 1

        # """ Receiving the filename from the client. """
        # filename = conn.recv(1024).decode()
        # print(f"[RECV] Receiving the filename.")
        # file = open(filename, "w")
        # conn.send("Filename received.".encode())

        # """ Receiving the file data from the client. """
        # data = conn.recv(1024).decode()
        # print(f"[RECV] Receiving the file data.")
        # file.write(data)
        # conn.send("File data received".encode())
        
        # """ Close the file"""
        # file.close()
        # """ Close the connection from the client"""
    
    conn.close()
    print(f"[DISCONNECTED] {address} disconnected.")


if __name__ == '__main__':
    server_program()

