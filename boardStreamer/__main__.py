import argparse

from find_cyton import find_cyton

from brainflow.board_shim import BoardShim, BoardIds, BrainFlowInputParams

from time import sleep

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

args = parser.parse_args()

# chooses between simulated board or real board
if args.mode in ['sim8', 'sim16']:
	board_args = BrainFlowInputParams()
	board = BoardShim(
		BoardIds.SYNTHETIC_BOARD,
		board_args
	)
else:
	board = find_cyton(lambda x : True)

board.prepare_session()
board.start_stream()

if args.mode == 'sim8':
	def aquire_data(board : BoardShim):
		
		eeg_channels = board.get_eeg_channels(board.board_id)[:8]

		return board.get_board_data(args.window)[eeg_channels,:]
elif args.mode == 'sim16':
	def aquire_data(board : BoardShim):
		
		eeg_channels = board.get_eeg_channels(board.board_id)[:16]

		return board.get_board_data(args.window)[eeg_channels,:]
else:
	def aquire_data(board : BoardShim):
		
		eeg_channels = board.get_eeg_channels(board.board_id)

		return board.get_board_data(args.window)[eeg_channels,:]

## Insert Socket Code ##



# Insert Code to aquire board data
while True:
	sleep(1)
	foo = aquire_data(board)
	pass