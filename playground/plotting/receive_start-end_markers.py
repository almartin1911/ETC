import serial
import time
import sys
import numpy


class Test(object):
    """docstring for Test."""

    def __init__(self):
        super(Test, self).__init__()
        port = '/dev/ttyACM0'
        self.arduino = serial.Serial(port, 9600)
        # time.sleep(2)

        self.num_bytes = 5
        self.received_bytes = numpy.empty(dtype=numpy.uint8,
                                          shape=self.num_bytes)
        # received_bytes = bytearray()

        self.new_data = False

    def receive(self):
        recv_in_progress = False
        ndx = 0
        start_marker = b'<'
        end_marker = b'>'
        received_byte = b''

        while not self.new_data:
            received_byte = self.arduino.read()
            print(received_byte, end=' ')

            if recv_in_progress:
                if received_byte != end_marker:
                    int_received_byte = int.from_bytes(received_byte,
                                                       byteorder=sys.byteorder)

                    self.received_bytes[ndx] = int_received_byte
                    ndx += 1

                    if ndx >= self.num_bytes:
                        ndx = self.num_bytes - 1
                else:
                    self.received_bytes[ndx] = 0
                    recv_in_progress = False
                    ndx = 0
                    self.new_data = True
            elif received_byte == start_marker:
                recv_in_progress = True

    def show_new_data(self):
        if self.new_data:
            # print("Habemus data:")
            # print(self.received_bytes.tobytes())
            print(self.received_bytes[:2])
            self.new_data = False


test = Test()
while 1:
    test.receive()
    test.show_new_data()
