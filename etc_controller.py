import etc_serial
import etc_plotcanvas

from color_constants import colors
import sys
import bitstring
import threading
import ctypes

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib


class Controller(object):
    def __init__(self, model, view):
        self._model = model

        # VIEW
        self._view = view
        # Left pane
        self._lpane = self._view._lpane
        self._frame_serial = self._lpane._frame_serial
        self._frame_parameters = self._lpane._frame_parameters
        self._frame_commands = self._lpane._frame_commands
        # Right pane
        self._rpane = self._view._rpane
        self._fboxplotcanvas = self._rpane._fboxplotcanvas

        # SERIAL
        self._frame_serial._progress_bar.set_text('Pulso de paquetes')
        t = None
        self._arduino = etc_serial.Serial(timeout=t)
        self._load_ports()
        self.is_connected = threading.Event()
        self.is_run = True
        self.read_thread = None
        # self.read_serial_start()

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
        # False parameter: no debug
        self._db_session = self._model.connect_to_database(False)
        self._parameters = self._get_parameters()
        # print(self._parameters, len(self._parameters))
        # TODO: Real management of commands and users
        self._command = self._db_session.query(self._model.Command).first()
        self._user_exec = self._db_session.query(self._model.User).first()
        self._setup_load_parameters()
        self._load_commands()

        # VIEW EVENTS
        self._frame_serial.connect('btn-refresh-clicked',
                                   self._on_btn_refresh_clicked)
        self._frame_serial.connect('cbox-ports-changed',
                                   self._on_cbox_ports_changed)
        self._frame_serial.connect('switch-serial-toggled',
                                   self._on_switch_serial_toggled)

        # C LIBRARY INTERACTION
        # TODO: Relative path
        self._lib = ctypes.CDLL(
            '/home/amartin1911/dev/ETC/libreria.so')

        self._view.show_all()

        # Draw empty canvases
        self._plotcanvas_list = []
        self.load_canvases()

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
                self.start_operations()
            else:
                print('Switch OFF')
                self.stop_operations()

    def start_operations(self):
        # self._db_session = self._model.connect_to_database(False)
        # self.thread = None
        self.is_run = True
        try:
            self.read_serial_start()
            self._arduino.open_port()
            self.is_connected.set()
            # print(self.thread)
        except Exception as e:
            print(e)
        # self.read_serial_start()

    def stop_operations(self):
        # Thread close
        self.is_run = False
        # print(self.read_thread)
        # # try:
        # #     self.read_thread.join()
        # # except Exception as e:
        # #     print(e)
        # # # self.read_thread.join()
        # print('OK')
        # Arduino close
        self._arduino.close()
        # Clear is_connected event (for reading) value
        self.is_connected.clear()

        # self.thread = None
        # SQLAlchemy session commiting and closing
        try:
            self._db_session.commit()
        except Exception as e:
            self._db_session.rollback()
            print(e)
        # finally:
        #     self._db_session.close()
        #     print(self._db_session)

        print('Disconnected...')

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

    def _update_progress_bar(self, ok, bad):
        self._frame_serial._progress_bar.pulse()
        self._frame_serial._progress_bar.set_text(str(ok) + u'\u2714' + ' '
                                                  + str(bad) + u'\u2716')
        return False

    # /////////////// Parameters ///////////////
    def _get_parameters(self):
        return self._db_session.query(self._model.Parameter).all()

    def _get_parameters_store(self):
        # Querying the db trough db_session
        # parameters = self._db_session.query(self._model.Parameter).all()
        parameters_store = Gtk.ListStore(str, str, str)

        # Populating parameters_store
        default_value = "0.00"
        for parameter in self._parameters:
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
        parameters_store = self._get_parameters_store()
        tv_parameters.set_model(parameters_store)

    # /////////////// Commands ///////////////
    def _get_commands(self):
        return self._db_session.query(self._model.Command).all()

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
        # self._arduino.reset_input_buffer()
        print('Waiting for connection...')
        # print(self.thread)
        self.is_connected.wait()
        print('Connected!')

        while self.is_run:
            try:
                self._arduino.readinto(self.raw_data)
                self.package_builder()
            except Exception as e:
                print(e)
                break
            # print(self.raw_data)

    def read_serial_start(self):
        # print("THREAD:", self.thread)
        # if self.thread is None:
        self.read_thread = threading.Thread(target=self.background_thread)
        self.read_thread.daemon = True
        self.read_thread.start()

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
                self.package_counter += 1
                self.handle_package()
                # checksum_value = bytes([self.package[self.package_size - 1]])
                #
                # if self.verify_checksum(checksum_value):
                #     self.package_counter += 1
                #     self.handle_package()
                # else:
                #     self.bad_package_counter += 1
                GLib.idle_add(self._update_progress_bar,
                              self.package_counter,
                              self.bad_package_counter)
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

    def handle_package(self):
        bitstream_package = bitstring.BitStream(self.package)
        # bitstream_package = bitstring.BitStream(self.package.tobytes())
        print('#', self.package_counter, ':', bitstream_package,
              len(bitstream_package))
        # print("Lost packages:", self.bad_package_counter)
        for value in self.package:
            print(value, end=' ')

        # Add raw record
        record = self._model.add_record(self._db_session,
                                        bitstream_package.hex,
                                        self._command, self._user_exec)

        # Parse package
        # Package_woh is package without the header
        package_woh = self.package[1:]
        # print(len(package_woh))
        c_chr_array_package = (ctypes.c_char
                               * len(package_woh))(*package_woh)
        # size = 16
        c_float_array_parsed = (ctypes.c_float * len(self._parameters))()
        # print(c_chr_array_package, len(c_chr_array_package), c_float_array_parsed, len(c_float_array_parsed))
        self.c_parse_package(c_chr_array_package,
                             len(c_chr_array_package),
                             c_float_array_parsed,
                             len(c_float_array_parsed))
        print()
        self.print_array(c_float_array_parsed)
        print()

        parsed_str_parameters = []
        for i in range(len(self._parameters)):
            parsed_str_parameters.append(f'{c_float_array_parsed[i]:.3f}')
            self._model.add_parameter_record(self._db_session,
                                             parsed_str_parameters[i],
                                             self._parameters[i],
                                             record)

        # Refresh tv_parameters
        GLib.idle_add(self.refresh_tv_parameters, parsed_str_parameters)
        # Plot data
        GLib.idle_add(self.refresh_plots, c_float_array_parsed)

    def c_parse_package(self, input, size_in, output, size_out):
        self._lib.parse_package.restype = ctypes.c_void_p
        self._lib.parse_package(input, size_in, output, size_out)

    def print_array(self, array):
        print(len(array), end=' | ')
        for value in array:
            print(format(value, '.2f'), end=', ')
        print()

    def refresh_tv_parameters(self, parsed_str_parameters):
        tv_parameters = self._frame_parameters._tv_parameters
        store_parameters = tv_parameters.get_model()

        rootiter = store_parameters.get_iter_first()
        store_parameters[rootiter][1] = parsed_str_parameters[0]

        treeiter = store_parameters.iter_next(rootiter)
        store_parameters[treeiter][1] = parsed_str_parameters[1]

        for i in range(2, len(self._parameters)):
                treeiter = store_parameters.iter_next(treeiter)
                store_parameters[treeiter][1] = parsed_str_parameters[i]

        tv_parameters.set_model(store_parameters)

        return False

    def load_canvases(self):
        flowbox = self._fboxplotcanvas._fb
        c = 0
        colors_list = [colors['cobalt'],
                       colors['cobaltgreen'],
                       colors['coldgrey'],
                       colors['cobalt'],
                       colors['cobaltgreen'],
                       colors['coldgrey'],
                       colors['cobalt'],
                       colors['cobaltgreen'],
                       colors['coldgrey'],
                       colors['cobalt'],
                       colors['cobaltgreen'],
                       colors['coldgrey'],
                       colors['cobalt'],
                       colors['cobaltgreen'],
                       colors['coldgrey'],
                       colors['cobalt']
                       ]

        for parameter in self._parameters:
            plotcanvas = etc_plotcanvas.PlotCanvas(parameter.name,
                                                   parameter.symbol,
                                                   parameter.unit,
                                                   colors_list[c].hex_format())
            self._plotcanvas_list.append(plotcanvas)
            flowbox.add(plotcanvas.canvas)
            c += 1

    def refresh_plots(self, c_float_array_parsed):
        for i in range(len(self._plotcanvas_list)):
            self._plotcanvas_list[i].update_draw(c_float_array_parsed[i])
