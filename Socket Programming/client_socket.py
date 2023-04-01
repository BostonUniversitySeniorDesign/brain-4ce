import socket
import time
import pickle
import pandas

# def sim_live_data():
#     file = open('out.csv','r')
#     count = 0

#     while True:
#         count += 1
        
#         #wait 1 second between each line
#         time.sleep(1)

#         # Get next line from file
#         line = file.readline()
 
#         # if line is empty
#         # end of file is reached
#         if not line:
#             break
 
#     file.close()

def client_program():
    host = socket.gethostname()
    port = 65400 #random unprivileged port

    """ Read file"""
    file = pandas.read_csv('out.csv')
    
    """ Starting a TCP socket. """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    """ Connecting to the server. """    
    client_socket.connect((host, port))

    # """ Opening and reading the file data. """
    # file = open("out.csv", "r")
    # data = file.read()
    
    # """ Sending the filename to the server. """
    # client_socket.send("out.csv".encode())
    # msg = client_socket.recv(1024).decode()
    # print(f"[SERVER]: {msg}")
 
    # """ Sending the file data to the server. """
    # client_socket.send(data.encode())
    # msg = client_socket.recv(1024).decode()
    # print(f"[SERVER]: {msg}")

    client_socket.send(bytes("Sending file...", 'utf-8'))

    Buffer = []

    for inx in range(file.shape[0]):
        Buffer = file.loc[inx]
        print(f"Sending \n {Buffer}")
        client_socket.send(pickle.dumps(Buffer))
        time.sleep(2)  # Wait 2 sec

    
        """ Close the file. """
        file.close()
    
        """ Close the connection from the server. """
        client_socket.close()


if __name__ == '__main__':
    client_program()