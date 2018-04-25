import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class ETC_Window_rpane(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
