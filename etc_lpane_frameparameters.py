import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Lpane_frameparameters(Gtk.Frame):
    def __init__(self):
        super(Lpane_frameparameters, self).__init__()
        self.set_label("Parámetros")

        self._grid = Gtk.Grid()
        self.add(self._grid)

        self._tv_parameters = Gtk.TreeView()
        self._grid.attach(self._tv_parameters, 0, 0, 1, 1)
