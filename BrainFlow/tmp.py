def main():
    s = "start 1220"
    print(s[6:len(s)])


#board_shim.stop_stream() to stop streaming
#get_current_board_data() - returns array of latest data stored in ringbuffer, does not clear ring buffer.
#get_board_data(int count) - gets num of elements in ring buffer
#insert_marker() - inserts marker to data stream
#get_board_data() gets all data and removes from ringbuffer

if __name__ == '__main__':
    main()