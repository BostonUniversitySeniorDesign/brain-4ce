import time
import random


def main():
    count = 0
    # How many numbers to generate 
    num_outputs = 5
    # How many seconds to wait until the next number
    sec_between = 1

    while count < num_outputs:
        num = int(random.uniform(1, 5))
        count += 1
        print(num)
        time.sleep(sec_between)

if __name__ == "__main__":
    main()