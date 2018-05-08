import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class ETC_window_frmcommands(Gtk.Frame):
    def __init__(self, controller):
        Gtk.Frame.__init__(self)
        self.set_label("Comandos")

        self.controller = controller

        flowbox = Gtk.FlowBox()
        self.add(flowbox)

        controller.load_commands(flowbox)
