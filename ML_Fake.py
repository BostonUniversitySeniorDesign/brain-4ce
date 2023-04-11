import time
import random
import socket


def s_main():
    count = 0
    # How many numbers to generate 
    num_outputs = 5
    # How many seconds to wait until the next number
    sec_between = 1

    # setup socket connection 
    host = socket.gethostname()
    port = 55002 #random unprivileged port
    """ Starting a TCP socket. """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    """ Connecting to the server. """    
    client_socket.connect((host, port))
    
    t_end = time.time() + 60
    #generate numbers for 60 seconds to give a better representation of data
    while time.time() < t_end:
        # while count < num_outputs:
        num = int(random.uniform(0, 3))
        count += 1
        client_socket.send(str(num).encode())
        # print(num)
        time.sleep(sec_between)


if __name__ == "__main__":
    s_main()