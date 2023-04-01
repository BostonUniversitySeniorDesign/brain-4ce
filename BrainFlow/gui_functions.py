import argparse
import logging
import sys
import numpy as np
import time
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds

#Input port_num as string ex. COM3
def init_board(port_num):
    BoardShim.enable_dev_board_logger()
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    # use docs to check which parameters are required for specific board, e.g. for Cyton - set serial port
    parser.add_argument('--timeout', type=int, help='timeout for device discovery or connection', required=False,
                        default=0)
    parser.add_argument('--ip-port', type=int, help='ip port', required=False, default=0)
    parser.add_argument('--ip-protocol', type=int, help='ip protocol, check IpProtocolType enum', required=False,
                        default=0)
    parser.add_argument('--ip-address', type=str, help='ip address', required=False, default='')
    parser.add_argument('--serial-port', type=str, help='serial port', required=False, default='COM9') #SERIAL PORT
    parser.add_argument('--mac-address', type=str, help='mac address', required=False, default='')
    parser.add_argument('--other-info', type=str, help='other info', required=False, default='')
    parser.add_argument('--streamer-params', type=str, help='streamer params', required=False, default='')
    parser.add_argument('--serial-number', type=str, help='serial number', required=False, default='')
    parser.add_argument('--board-id', type=int, help='board id, check docs to get a list of supported boards',
                        required=False, default=BoardIds.CYTON_BOARD) #BOARD ID HERE - CHANGE FOR CYTON
    parser.add_argument('--file', type=str, help='file', required=False, default='')
    parser.add_argument('--master-board', type=int, help='master board id for streaming and playback boards',
                        required=False, default=BoardIds.NO_BOARD)
    args = parser.parse_args()

    params = BrainFlowInputParams()
    params.ip_port = args.ip_port
    params.serial_port = port_num
    params.mac_address = args.mac_address
    params.other_info = args.other_info
    params.serial_number = args.serial_number
    params.ip_address = args.ip_address
    params.ip_protocol = args.ip_protocol
    params.timeout = args.timeout
    params.file = args.file
    params.master_board = args.master_board

    #define board_shim globally
    global board_shim;
    board_shim = BoardShim(args.board_id, params) #initiate board with params and ID
    board_shim.prepare_session() #need this to prepare streaming session

#Make a class that has arrays for each task
#Parameters to store subject no. and data type (real vs mi) 
#Create a constructor that takes subject no. and data type inputs
#Create an update function that updates the values for a given matrix
#Create a function that saves all of the data into a single file
#Function that returns all data
#include board in this class?


class dataclass():
    #Create arrays for each task
    task0 = []
    task1 = []
    task2 = []
    task3 = []
    task4 = []
    task5 = []