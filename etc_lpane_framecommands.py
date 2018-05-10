import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Lpane_framecommands(Gtk.Frame):
    def __init__(self):
        super(Lpane_framecommands, self).__init__()
        self.set_label("Comandos")

        self._flowbox = Gtk.FlowBox()
        self.add(self._flowbox)

        # controller.load_commands(flowbox)
