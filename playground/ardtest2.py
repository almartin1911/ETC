# NOTE: Needs an Arduino program which sends "package_size" sized data
# with a "header" header.
# ls /dev/tty*

import threading
import serial
import sys
# import os
# import time
import bitstring
# import queue
# import numpy
import faulthandler
faulthandler.enable()

import matplotlib as mpl
mpl.use('GTK3Agg')
import matplotlib.pyplot as plt

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

import matplotlib as mpl
mpl.use('GTK3Agg')
from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)
from matplotlib.figure import Figure


class PlotWindow(Gtk.Window):
    def __init__(self):
        super(PlotWindow, self).__init__()
        self.connect('destroy', Gtk.main_quit)

        self.box = Gtk.Box(spacing=6, orientation=Gtk.Orientation(1))
        self.add(self.box)

        self.switch = Gtk.Switch()
        self.switch.connect("notify::active", self.on_switch_toggled)
        self.switch.set_active(False)
        self.box.pack_start(self.switch, True, True, 0)

        self.progress = Gtk.ProgressBar(show_text=True)
        self.box.pack_start(self.progress, True, True, 0)

        # global line, ax, canvas
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(0, 30)
        self.ax.set_ylim([0, 255])
        self.ax.set_autoscale_on(False)
        self.data = []
        self.l_data, = self.ax.plot([], self.data, label='MagY')
        self.ax.legend()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.set_size_request(800, 600)
        self.canvas.show()
        self.box.pack_start(self.canvas, True, True, 0)
        # self.line, = self.ax.plot([1, 2, 3], [1, 2, 10])

        port = '/dev/ttyACM0'
        baud = 9600
        self.arduino = ArdTest(self, port, baud)
        # arduino.open_conn()

    def on_switch_toggled(self, switch, gparam):
        if switch.get_active():
            state = "on"
            self.arduino.open_conn()
        else:
            state = "off"
            self.arduino.close()
        print("Switch was turned", state)

    def update_progress(self, ok, bad):
        self.progress.pulse()
        self.progress.set_text(str(ok) + ' OK, ' + str(bad) + ' BAD')
        return False

    def update_plot(self, result):
        # print(threading.current_thread().getName())
        # self.line.set_ydata([1, result, 10])
        # self.ax.draw_artist(self.line)
        # self.canvas.draw()
        self.data.append(result)
        # print(self.data)
        self.l_data.set_data(range(len(self.data)), self.data)
        # print(self.l_data)
        try:
            self.canvas.draw()
        except Exception as e:
            print(e)
        return False


class ArdTest(object):
    def __init__(self, view, port='/dev/ttyACM0', baud=9600):
        super(ArdTest, self).__init__()
        self.view = view
        print(view)
        self.port = port
        self.baud = baud

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

        # self.thread = None
        self.is_run = True
        self.is_connected = threading.Event()
        self.thread = threading.Thread(target=self.background_thread)
        self.thread.daemon = True
        self.thread.start()

        # self.read_serial_start()

        # print(f'Trying connection at {self.port} with {self.baud} baudrate...')
        # try:
        #     self.serial_connection = serial.Serial(port, baud)
        #     self.is_connected.set()
        #     print('Succesful connection!')
        # except Exception as e:
        #     print('Failed to connect')

    def open_conn(self):
        print(f'Trying connection at {self.port} with {self.baud} baudrate...')
        try:
            self.serial_connection = serial.Serial(self.port, self.baud)
            self.is_connected.set()
            print('Succesful connection!')
        except Exception as e:
            print('Failed to connect')

    def background_thread(self):
        # self.serial_connection.reset_input_buffer()
        print('Esperando conexión...')
        self.is_connected.wait()

        # while self.serial_connection.is_open and self.is_run:
        while self.is_run:
            try:
                self.serial_connection.readinto(self.raw_data)
            except Exception as e:
                print(e)
                break
            # print(self.raw_data)
            self.package_builder()
            # self.is_receiving = True
        # print(threading.enumerate())
        # self.close()

    # def read_serial_start(self):
    #     # if self.thread is None:
    #     self.thread = threading.Thread(target=self.background_thread)
    #     self.thread.start()

    # TODO: Use next function logic to gracefully end the thread
    def close(self):
        print(self.thread.name)
        self.is_run = False
        self.thread.join()
        # self.serial_connection.close()
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
                    # print(threading.current_thread().name)
                    # self.package_queue.put(self.buffer)
                    self.print_package()
                    # print(self.buffer[1])
                    # print(type(self.buffer[1]))
                    # self.view.update_plot(self.buffer[1])
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
        GLib.idle_add(self.view.update_progress, self.buffer_counter, self.bad_buffer_counter)
        GLib.idle_add(self.view.update_plot, self.buffer[1])

    def return_buffer(self):
        return self.buffer


def main():
    # port = '/dev/ttyACM0'
    # baud = 9600
    # arduino = ArdTest(port, baud)
    # arduino.open_conn()
    win = PlotWindow()
    win.show_all()
    Gtk.main()


if __name__ == '__main__':
    main()

# (ardtest2.py:14489): Gdk-ERROR **: 23:59:45.348: The program 'ardtest2.py' received an X Window System error.
# This probably reflects a bug in the program.
# The error was 'RenderBadPicture (invalid Picture parameter)'.
#   (Details: serial 4023 error_code 143 request_code 139 (RENDER) minor_code 26)
#   (Note to programmers: normally, X errors are reported asynchronously;
#    that is, you will receive the error a while after causing it.
#    To debug your program, run it with the GDK_SYNCHRONIZE environment
#    variable to change this behavior. You can then get a meaningful
#    backtrace from your debugger if you break on the gdk_x_error() function.)
# Trace/breakpoint trap (core dumped)
