# NOTE: Needs an Arduino program which sends "package_size" sized data
# with a "header" header.
# ls /dev/tty*

import threading
import serial
import sys
# import os
import time
import bitstring
import numpy


class ArdTest(object):
    def __init__(self, port='/dev/ttyACM0', baud=9600):
        super(ArdTest, self).__init__()
        self.port = port
        self.baud = baud

        self.is_run = True
        self.is_receiving = False
        self.thread = None

        self.raw_data = bytearray(1)
        # Next won't work since pyserial readline needs a bytearray or array
        # self.raw_data = b''

        self.header = b'\xd1'
        self.buffer_size = 31
        # self.buffer = numpy.empty(dtype=numpy.uint8, shape=self.buffer_size)
        self.buffer = bytearray(self.buffer_size)
        self.buffer_counter = 0
        self.buffer_pointer = 0

        self.is_header = False
        self.first_time_header = False

        self.bad_buffer_counter = 0

        print(f'Trying connection at {self.port} with {self.baud} baudrate...')
        try:
            self.serial_connection = serial.Serial(port, baud, timeout=4)
            print('Succesful connection!')
        except Exception as e:
            print('Failed to connect')

    def background_thread(self):
        self.serial_connection.reset_input_buffer()
        while self.is_run:
            self.serial_connection.readinto(self.raw_data)
            # print(self.raw_data)
            self.package_builder()
            self.is_receiving = True

    def read_serial_start(self):
        if self.thread is None:
            self.thread = threading.Thread(target=self.background_thread)
            self.thread.start()
            # try:
            #     self.thread.start()
            # except(KeyboardInterrupt, SystemExit):
            #     self.close()

            # Block till we start receiving values
            while self.is_receiving is not True:
                time.sleep(0.1)

    # TODO: Use next function logic to gracefully end the thread
    def close(self):
        self.is_run = False
        self.thread.join()
        self.serial_connection.close()
        print('Disconnected...')

    def package_builder(self):
        received_byte = self.raw_data
        # print(self.buffer_pointer, received_byte, end=", ")

        if received_byte == self.header:
            if not self.first_time_header:
                self.is_header = True
                self.buffer_pointer = 0
                self.first_time_header = True

        int_received_byte = int.from_bytes(received_byte,
                                           byteorder=sys.byteorder)
        self.buffer[self.buffer_pointer] = int_received_byte
        self.buffer_pointer += 1

        if self.buffer_pointer >= self.buffer_size:
            self.buffer_pointer = 0

            if self.is_header:
                checksum_value = bytes([self.buffer[self.buffer_size - 1]])

                if self.verify_checksum(checksum_value):
                    self.buffer_counter += 1
                    self.print_package()
                else:
                    self.bad_buffer_counter += 1

                self.is_header = False
                self.first_time_header = False

    def verify_checksum(self, orig_result):
        result = b''
        mask = b'\xff'
        sum = 0

        for i in range(self.buffer_size - 1):
            # num = int.from_bytes(self.buffer[i], byteorder=sys.byteorder)
            sum += self.buffer[i]

        result = bytes([sum.to_bytes(4, sys.byteorder)[0] & mask[0]])
        # print(result, orig_result)

        if orig_result == result:
            return True
        else:
            return False

    def print_package(self):
        bitstream_buffer = bitstring.BitStream(self.buffer)
        # bitstream_buffer = bitstring.BitStream(self.buffer.tobytes())
        print('#', self.buffer_counter, ':', bitstream_buffer,
              len(bitstream_buffer))
        print("Lost packages:", self.bad_buffer_counter)

    def return_buffer(self):
        return self.buffer


def main():
    port = '/dev/ttyACM0'
    baud = 38400
    arduino = ArdTest(port, baud)
    arduino.read_serial_start()


if __name__ == '__main__':
    main()
    # try:
    #     # main()
    #     port = '/dev/ttyACM0'
    #     baud = 9600
    #     arduino = ArdTest(port, baud)
    #     arduino.read_serial_start()
    #
    # except KeyboardInterrupt:
    #     print('Interrupted')
    #     arduino.close()
    #     try:
    #         sys.exit(0)
    #     except SystemExit:
    #         os._exit(0)
