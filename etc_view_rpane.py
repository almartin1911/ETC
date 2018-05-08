import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class View_rpane(Gtk.Grid):
    def __init__(self):
        super(View_rpane, self).__init__()
