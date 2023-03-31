import serial

from serial.tools.list_ports import comports
from time import sleep

from typing import Callable

from brainflow.board_shim import BoardShim, BoardIds, BrainFlowInputParams


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

	with serial.Serial(cyton.device, baudrate=115_200) as probe:

		# attempts to set board to 16 channels
		# meaning I am checking for the existance of a daisy
		probe.write(b'C')
		response = probe.read(2)

		# flushes buffered COM IO
		probe.read_all()

		# checks the response form the request
		# b'16 indicates it has a daisy
		if response == b'16':
			return init_daisy(cyton)
		elif response == b'no':
			return init_cyton(cyton)
		else:
			raise Exception(f'unknown hardware configuration on {cyton.device}')
	
def init_daisy(cyton):

	return BoardShim(
		board_id     = BoardIds.CYTON_DAISY_BOARD,
		input_params = BrainFlowInputParams(
			serial_port = cyton.device
		)
	)

def init_cyton(cyton):

	brd_params = BrainFlowInputParams()

	brd_params.serial_port = cyton.device

	return BoardShim(
		board_id     = BoardIds.CYTON_BOARD,
		input_params = brd_params
	)

if __name__ == '__main__':
	main()