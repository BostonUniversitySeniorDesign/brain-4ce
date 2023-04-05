import argparse
from find_cyton import find_cyton
from brainflow.board_shim import BoardShim, BoardIds, BrainFlowInputParams
from time import sleep

from functools import cached_property

parser = argparse.ArgumentParser(
	prog='Board Streamer',
	description='Connect to a real EEG board or simulates an EEG board to send data over a socker',
	# epilog='Text at the bottom of help'
)

parser.add_argument(
	'-p', '--port',
	type=int,
	default=800,
	help='Port to send data to over sockets'
)

parser.add_argument(
	'-m', '--mode',
	choices=['sim8', 'sim16', 'com'],
	default='com',
	help='sets server mode'
)

parser.add_argument(
	'-w', '--window',
	type=int,
	default=10,
	help='determines the number of samples to aquire per packet'
)

'''
	Returns list for keyword arguments
'''
args = parser.parse_args()
args = vars(args)

class CytonBoard:
	def __init__(self, mode='com', window=10, **kargs):

		self.mode   : str = mode
		self.window : int = window

	@cached_property
	def board(self) -> BoardShim:
		'''
			creates brainflow board instance
		'''
		
		# chooses between simulated board or real board
		if self.mode in ['sim8', 'sim16']:
			board_args = BrainFlowInputParams()
			board = BoardShim(
				BoardIds.SYNTHETIC_BOARD,
				board_args
			)
		else:
			board = find_cyton(lambda x : True)

		board.prepare_session()
		board.start_stream()

		return board

	@cached_property
	def eeg_channels(self) -> list:
		'''
			Gets indices from the data packets that correspond to
			EEG channels
		'''

		if self.mode == 'sim8':
			return self.board.get_eeg_channels(self.board.board_id)[:8]
		elif self.mode == 'sim16':
			return self.board.get_eeg_channels(self.board.board_id)[:16]
		else:
			return self.board.get_eeg_channels(self.board.board_id)

	def get_data(self) -> list:
		'''
			Gets next data of size self.window
		'''

		# brings function to get amount of data in the ring buffer
		# into the local scope
		num_samples = self.board.get_board_data_count

		while num_samples() < self.window: 
			sleep(0.004) # 4ms sleep since sample rate is 250 Hz
		
		return self.board.get_board_data(self.window)[self.eeg_channels,:]


board = CytonBoard(**args)

while True:
	data = board.get_data()

	# insert socket code here
