import etc_serial
# import etc_packages

import sys
import bitstring
import threading
# import time
import ctypes

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Controller(object):
    def __init__(self, model, view):
        self._model = model

        # VIEW
        self._view = view
        self._lpane = self._view._lpane
        self._frame_serial = self._lpane._frame_serial
        self._frame_parameters = self._lpane._frame_parameters
        self._frame_commands = self._lpane._frame_commands

        # SERIAL
        self._arduino = etc_serial.Serial()
        self._load_ports()
        # self._read_thread = threading.Thread(
        #     target=self._read_data_from_serial)
        self.is_run = True
        self.is_receiving = False
        self.thread = None

        self.raw_data = bytearray(1)
        self.header = b'\xd1'
        self.package_size = 31
        # self.package = numpy.empty(dtype=numpy.uint8,
        #                            shape=self.package_size)
        self.package = bytearray(self.package_size)
        self.package_counter = 0
        self.package_pointer = 0

        self.is_header = False
        self.first_time_header = False

        self.bad_package_counter = 0

        # DATABASE
        self._db_session = self._model.connect_to_database(False)
        self._setup_load_parameters()
        self._load_commands()

        # VIEW EVENTS
        self._frame_serial.connect('btn-refresh-clicked',
                                   self._on_btn_refresh_clicked)
        self._frame_serial.connect('cbox-ports-changed',
                                   self._on_cbox_ports_changed)
        self._frame_serial.connect('switch-serial-toggled',
                                   self._on_switch_serial_toggled)

        # TODO> Relative path
        self._lib = ctypes.CDLL(
            '/home/amartin1911/dev/ETC/playground/cpython/libreria.so')

        self._view.show_all()

    # /////////////// Serial ///////////////
    def _on_btn_refresh_clicked(self, button):
        # TODO: How to get the name of the button?
        print('Refresh clicked')
        self._load_ports()

    def _on_cbox_ports_changed(self, cbox):
        print('Cbox ports changed')
        self._set_port()

    def _on_switch_serial_toggled(self, widget, active):
            if active is True:
                print('Switch ON')
                self._arduino.open_port()
                self.read_serial_start()
            else:
                print('Switch OFF')
                self.close_connection()

    def _get_available_serial_ports(self):
        ports = self._arduino.list_serial_ports()
        ports_store = Gtk.ListStore(str)

        for port in ports:
            ports_store.append([port])

        return ports_store

    def _load_ports(self):
        # Loading and setting a data model for cbox_ports
        ports_store = self._get_available_serial_ports()
        cbox_ports = self._frame_serial._cbox_ports
        cbox_ports.set_model(ports_store)
        cbox_ports.set_active(0)

        self._set_port()

    def _set_port(self):
        cbox_ports = self._frame_serial._cbox_ports

        try:
            treeiter = cbox_ports.get_active_iter()
            model = cbox_ports.get_model()
            # Setting the port for the serial device
            self._arduino.port = model[treeiter][0]
        except TypeError:
            print("No connected devices")

    # /////////////// Parameters ///////////////
    def _get_parameters(self):
        # Querying the db trough db_session
        parameters = self._db_session.query(self._model.Parameter).all()
        parameters_store = Gtk.ListStore(str, str, str)

        # Populating parameters_store
        default_value = "0"
        for parameter in parameters:
            symbol = parameter.symbol
            unit = parameter.unit
            parameters_store.append([symbol, default_value, unit])

        return parameters_store

    def _setup_load_parameters(self):
        tv_parameters = self._frame_parameters._tv_parameters
        # Setting headings and a text renderer for each column
        columns = ["Simbolo", "Valor", "Unidad"]
        for i, column_title in enumerate(columns):
            renderer_text = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer_text, text=i)
            tv_parameters.append_column(column)

        # Loading and setting a model for the treeview
        parameters_store = self._get_parameters()
        tv_parameters.set_model(parameters_store)

    # /////////////// Commands ///////////////
    def _get_commands(self):
        commands_list = self._db_session.query(self._model.Command).all()

        return commands_list

    def _load_commands(self):
        flowbox = self._frame_commands._flowbox
        commands_list = self._get_commands()

        for command in commands_list:
            button = Gtk.Button()
            button.set_label(command.name)
            button.connect("clicked",
                           self._on_btn_command_clicked,
                           command)
            flowbox.add(button)

    def _on_btn_command_clicked(self, button, command):
        print(command)  # command is an object!

        str_command = command.command
        bytes_str_command = bytes.fromhex(str_command)

        self._arduino.write(bytes_str_command)
        print("Command sent:", bytes_str_command)

    # /////////////// Read data ///////////////
    def background_thread(self):
        self._arduino.reset_input_buffer()
        while self.is_run:
            self._arduino.readinto(self.raw_data)
            # print(self.raw_data)
            self.package_builder()
            self.is_receiving = True

    def read_serial_start(self):
        if self.thread is None:
            self.thread = threading.Thread(target=self.background_thread)
            self.thread.start()

            # Block till we start receiving values
            # while self.is_receiving is not True:
            #     time.sleep(0.1)

    # TODO: Use next function logic to gracefully end the thread
    def close_connection(self):
        self.is_run = False
        self.thread.join()
        self._arduino.close()
        print('Disconnected...')

    def package_builder(self):
        received_byte = self.raw_data
        # print(self.package_pointer, received_byte, end=", ")

        if received_byte == self.header:
            if not self.first_time_header:
                self.is_header = True
                self.package_pointer = 0
                self.first_time_header = True

        int_received_byte = int.from_bytes(received_byte,
                                           byteorder=sys.byteorder)
        self.package[self.package_pointer] = int_received_byte
        self.package_pointer += 1

        if self.package_pointer >= self.package_size:
            self.package_pointer = 0

            if self.is_header:
                checksum_value = bytes([self.package[self.package_size - 1]])

                if self.verify_checksum(checksum_value):
                    self.package_counter += 1
                    self.print_package()
                else:
                    self.bad_package_counter += 1

                self.is_header = False
                self.first_time_header = False

    def verify_checksum(self, orig_result):
        result = b''
        mask = b'\xff'
        sum = 0

        for i in range(self.package_size - 1):
            # num = int.from_bytes(self.package[i], byteorder=sys.byteorder)
            sum += self.package[i]

        result = bytes([sum.to_bytes(4, sys.byteorder)[0] & mask[0]])
        # print(result, orig_result)

        if orig_result == result:
            return True
        else:
            return False

    def print_package(self):
        bitstream_package = bitstring.BitStream(self.package)
        # bitstream_package = bitstring.BitStream(self.package.tobytes())
        print('#', self.package_counter, ':', bitstream_package,
              len(bitstream_package))
        print("Lost packages:", self.bad_package_counter)

        # Add raw record
        # TODO: Real management of commands and users
        command = self._db_session.query(self._model.Command).first()
        user_exec = self._db_session.query(self._model.User).first()

        # self._model.add_record(self._db_session, package,
        #                        command, user_exec)
        self._model.add_record(self._db_session, bitstream_package.hex,
                               command, user_exec)

        # Parse package
        c_chr_array_package = (ctypes.c_char
                               * len(self.package))(*self.package)
        size = 16
        c_float_array_parsed = (ctypes.c_float * size)()
        self.c_convierte(c_chr_array_package,
                         len(c_chr_array_package),
                         c_float_array_parsed,
                         len(c_float_array_parsed))
        self.print_array(c_float_array_parsed)

    def c_convierte(self, input, size_in, output, size_out):
        self._lib.convierte.restype = ctypes.c_void_p
        self._lib.convierte(input, size_in, output, size_out)

    def print_array(self, array):
        print(len(array), end=' | ')
        for value in array:
            print(format(value, '.2f'), end=', ')
        print()
