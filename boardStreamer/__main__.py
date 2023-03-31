import serial

from serial.tools.list_ports import comports
from time import sleep

from typing import Callable


def main():
    board = find_cyton(lambda x : True)

    print(board)

def find_cyton(criterion : Callable, duration=0.1):
    '''
        attempts to find cyton in com ports based on
        a passed criterion for a cyton
    '''

    # infinitely checkes for cyton
    while True:

        # gets cyton boards matching a certin pattern
        cyton_coms = list(filter(criterion, comports()))

        if len(cyton_coms) > 0:
            return resolve_cyton(cyton_coms)

        # sleeps then attempts to find a 
        sleep(duration)

def resolve_cyton(cyton_coms : list):
    '''
        takes the list of matched cyton boards and attempts to
        correctly initialize the board based on whether or not
        there is a Daisy module present
    '''

    # checks if multiple Cytons are detected
    if len(cyton_coms) > 1:
        raise Exception("Only supports 1 Cyton for now")

    return get_cyton(cyton_coms[0])

def get_cyton(cyton):
    '''
        initializes cyton correctly and returns a 
    '''

    # prevents reading startup message when connecting
    sleep(1)

    # attempts to connect to Cyton's serial port
    try:
        probe = serial.Serial(cyton.device, baudrate=115_200)
    except:
        raise Exception(f'Cound not connect to {cyton.device}')
    
    # attempts to set board to 16 channels
    # meaning I am checking for the existance of a daisy
    probe.write(b'C')
    response = probe.read(2)

    # checks the response form the request
    # b'16 indicates it has a daisy
    if response == b'16':
        return init_daisy(cyton)
    else:
        return init_cyton(cyton)
    
def init_daisy(cyton):
    pass

def init_cyton(cyton):
    pass

if __name__ == '__main__':
    main()