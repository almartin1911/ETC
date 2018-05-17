# Based on:
# http://www.toptechboy.com/tutorial/python-with-arduino-lesson-11-plotting-and-graphing-live-data-from-arduino-with-matplotlib/
# and Arduino forums read 
import serial
import time
import sys
import numpy
import matplotlib.pyplot as plt
import drawnow


class PlotTest(object):
    """docstring for PlotTest."""

    def __init__(self):
        super(PlotTest, self).__init__()
        port = '/dev/ttyACM0'
        self.arduino = serial.Serial(port, 9600)
        # time.sleep(2)

        self.num_bytes = 5
        self.received_bytes = numpy.empty(dtype=numpy.uint8,
                                          shape=self.num_bytes)

        self.new_data = False

        self.data_0 = []
        self.data_1 = []
        plt.ion()
        self.cnt = 0

    def make_fig(self):
        plt.ylim(0, 400)
        plt.title('Plot Test')
        plt.grid(True)
        plt.ylabel('Data 0')
        plt.plot(self.data_0, 'ro-', label='Data 0')
        plt.legend(loc='upper left')
        plt2 = plt.twinx()
        plt.ylim(0, 400)
        plt2.plot(self.data_1, 'b^-', label='Data 1')
        plt2.set_ylabel('Data 1')
        plt2.ticklabel_format(useOffset=False)
        plt2.legend(loc='upper right')

    def receive(self):
        recv_in_progress = False
        ndx = 0
        start_marker = b'<'
        end_marker = b'>'
        received_byte = b''

        while not self.new_data:
            received_byte = self.arduino.read()
            # print(received_byte)

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

            self.data_0.append(self.received_bytes[0])
            self.data_1.append(self.received_bytes[1])
            drawnow.drawnow(self.make_fig)
            plt.pause(.000001)
            self.cnt += 1
            if self.cnt > 50:
                self.data_0.pop(0)
                self.data_1.pop(0)

            self.new_data = False


test = PlotTest()
while 1:
    test.receive()
    test.show_new_data()
