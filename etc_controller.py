import etc_serial
import etc_model
from sqlalchemy import create_engine
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class ETC_controller():
    def __init__(self):
        self.arduino = etc_serial.ETC_Serial()
        self.db_session = self.connect_to_database()

    # /////////////// Serial ///////////////
    def get_available_serial_ports(self):
        ports = self.arduino.list_serial_ports()
        ports_store = Gtk.ListStore(str)

        for i in ports:
            ports_store.append([i])

        return ports_store

    def load_ports(self, cbox):
        # Loading and setting a data model for the cbox
        ports_store = self.get_available_serial_ports()
        cbox.set_model(ports_store)
        cbox.set_active(0)

        self.set_port(cbox)

    def set_port(self, cbox):
        try:
            treeiter = cbox.get_active_iter()
            model = cbox.get_model()
            # Setting the port for the serial device
            self.arduino.port = model[treeiter][0]
        except Exception as e:
            print(e)

    # /////////////// Database ///////////////
    def setup_database(self, engine):
        etc_model.Base.metadata.create_all(engine)
        print("Database sucessfully created")

    def connect_to_database(self):
        db_path = "sqlite:///etc_database.db"
        # echo=True for debugging purposes
        engine = create_engine(db_path, encoding="utf-8", echo=True)
        etc_model.init_model(engine)
        db_session = etc_model.DBSession()
        self.setup_database(engine)

        return db_session

    # /////////////// Parameters ///////////////
    def get_parameters(self):
        # Querying the db trough db_session
        parameters = self.db_session.query(etc_model.Parameter).all()
        parameters_store = Gtk.ListStore(str, str, str)

        # Populating parameters_store
        default_value = "0"
        for parameter in parameters:
            symbol = parameter.symbol
            unit = parameter.unit
            parameters_store.append([symbol, default_value, unit])

        return parameters_store

    def setup_load_parameters(self, treeview):
        # Setting headings and a text renderer for each column
        columns = ["Simbolo", "Valor", "Unidad"]
        for i, column_title in enumerate(columns):
            renderer_text = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer_text, text=i)
            treeview.append_column(column)

        # Loading and setting a model for the treeview
        parameters_store = self.get_parameters()
        treeview.set_model(parameters_store)

    # /////////////// Commands ///////////////
    def get_commands(self):
        commands = self.db_session.query(etc_model.Command).all()
        return commands

    def load_commands(self, flowbox):
        commands_list = self.get_commands()

        for command in commands_list:
            button = Gtk.Button()
            button.set_label(command.name)
            button.connect("clicked",
                           self.on_btn_command_clicked,
                           command)
            flowbox.add(button)

    def on_btn_command_clicked(self, button, command):
        print(command)  # command is an object!

        str_command = command.command
        bytes_str_command = bytes.fromhex(str_command)

        self.arduino.write(bytes_str_command)
        print("Command sent:", bytes_str_command)

        # try:
        #     self.arduino.write(raw_command)
        #     # FIXME: FOUND THE FAQIN' BUG!!!
        #     # while self.arduino.is_open:
        #     #     if self.arduino.in_waiting > 0:
        #     #         print(self.arduino.read())
        # except Exception as e:
        #     print(e)

    def read_data_from_serial(self):
        header = b'\xd1'

        package = b''

        package_counter = 0
        buffer_size = 32
        package_pointer = 0

        is_header = False
        first_time_header = False

        while self.arduino.in_waiting > 0:
            print(self.arduino.in_waiting)
            received_byte = self.arduino.read()

            if received_byte == header:
                if not first_time_header:
                    is_header = True
                    package_pointer = 0
                    first_time_header = True

            package += received_byte
            package_pointer += 1

            if package_pointer > buffer_size:
                package_pointer = 0

                if is_header:
                    package_counter += 1
                    print(package_counter, package)

                    package = b''

                    is_header = False
                    first_time_header = False
