import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class ETC_window_frmparameters(Gtk.Frame):
    def __init__(self, controller):
        Gtk.Frame.__init__(self)
        self.set_label("Parámetros")

        self.controller = controller

        grid = Gtk.Grid()
        self.add(grid)

        self.tv_parameters = Gtk.TreeView()
        self.controller.setup_load_parameters(self.tv_parameters)
        grid.attach(self.tv_parameters, 0, 0, 1, 1)
