import etc_serial

import sys
import bitstring
import threading

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Controller(object):
    def __init__(self, model, view):
        self._model = model

        self._view = view
        self._lpane = self._view._lpane
        self._frame_serial = self._lpane._frame_serial
        self._frame_parameters = self._lpane._frame_parameters

        self._arduino = etc_serial.Serial()
        self._load_ports()
        self._read_thread = threading.Thread(
            target=self._read_data_from_serial)

        self._db_session = self._model.connect_to_database()
        self._setup_load_parameters()

        self._frame_serial.connect('btn-refresh-clicked',
                                   self._on_btn_refresh_clicked)
        self._frame_serial.connect('cbox-ports-changed',
                                   self._on_cbox_ports_changed)
        self._frame_serial.connect('notify::active',
                                   self._on_switch_serial_toggled)

        self._view.show_all()

    # /////////////// Serial ///////////////
    def _on_btn_refresh_clicked(self, button):
        # TODO: How to get the name of the button?
        print('Refresh clicked')
        self._load_ports()

    def _on_cbox_ports_changed(self, cbox):
        print('Cbox ports changed')
        self._set_port()

    def _on_switch_serial_toggled(self, switch, state):
            if self._frame_serial._switch_serial.get_active():
                print('Switch ON')
                self._arduino.open_port()
                self._read_thread.start()
            else:
                print('Switch OFF')
                self._arduino.close_port()

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
    # def get_commands(self):
    #     commands = self.db_session.query(etc_model.Command).all()
    #     return commands
    #
    # def load_commands(self, flowbox):
    #     commands_list = self.get_commands()
    #
    #     for command in commands_list:
    #         button = Gtk.Button()
    #         button.set_label(command.name)
    #         button.connect("clicked",
    #                        self.on_btn_command_clicked,
    #                        command)
    #         flowbox.add(button)
    #
    # def on_btn_command_clicked(self, button, command):
    #     print(command)  # command is an object!
    #
    #     str_command = command.command
    #     bytes_str_command = bytes.fromhex(str_command)
    #
    #     self.arduino.write(bytes_str_command)
    #     print("Command sent:", bytes_str_command)
    #
    # /////////////// Read data ///////////////
    def _read_data_from_serial(self):
        header = b'\xd1'

        package = bytearray()

        package_counter = 0
        buffer_size = 32
        package_pointer = 0

        is_header = False
        first_time_header = False

        while self._arduino.is_open:
            # while arduino.in_waiting > 0: BUG: CAUSES 100% CPU CONSUMPTION
            received_byte = self._arduino.read()
            # print(package_pointer, received_byte, end=", ")

            if received_byte == header:
                if not first_time_header:
                    is_header = True
                    package_pointer = 0
                    first_time_header = True
                    package = bytearray()

            int_received_byte = int.from_bytes(received_byte,
                                               byteorder=sys.byteorder)
            package.append(int_received_byte)
            package_pointer += 1

            if package_pointer >= buffer_size:
                package_pointer = 0

                if is_header:
                    package_counter += 1
                    self.handle_package(package_counter, package)

                    is_header = False
                    first_time_header = False

    def handle_package(self, package_counter, package):
        bitstream_package = bitstring.BitStream(package)
        print('#', package_counter, ':', bitstream_package,
              len(bitstream_package))

        # TODO: Real management of commands and users
        # BUG: SQLAlchemy works on one thread only
        # command = self.db_session.query(etc_model.Command).first()
        # user_exec = self.db_session.query(etc_model.User).first()
        #
        # etc_model.add_record(self.session, bitstream_package.hex,
        #                      command, user_exec)
