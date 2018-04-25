import etc_serial
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class ETC_controller():
    def __init__(self):
        self.arduino = etc_serial.ETC_Serial()

    def get_available_serial_ports(self):
        ports = self.arduino.list_serial_ports()
        store_ports = Gtk.ListStore(str)

        for i in ports:
            store_ports.append([i])

        return store_ports

    def load_ports(self, cbox):
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
