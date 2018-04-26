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
        store_ports = Gtk.ListStore(str)

        for i in ports:
            store_ports.append([i])

        return store_ports

    def load_ports(self, cbox):
        # Loading and setting a data model for the cbox
        store_ports = self.get_available_serial_ports()
        cbox.set_model(store_ports)
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
        store_parameters = Gtk.ListStore(str, str, str)

        # Populating store_parameters
        default_value = "0"
        for parameter in parameters:
            symbol = parameter.symbol
            unit = parameter.unit
            store_parameters.append([symbol, default_value, unit])

        return store_parameters

    def setup_load_parameters(self, treeview):
        # Setting headings and a text renderer for each column
        columns = ["Simbolo", "Valor", "Unidad"]
        for i, column_title in enumerate(columns):
            renderer_text = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer_text, text=i)
            treeview.append_column(column)

        # Loading and setting a model for the treeview
        store_parameters = self.get_parameters()
        treeview.set_model(store_parameters)
