import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Rpane_osmgpsmap(Gtk.Frame):
    def __init__(self):
        super(Rpane_osmgpsmap, self).__init__()
