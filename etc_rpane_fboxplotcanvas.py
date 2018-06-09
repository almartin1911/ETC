# FlowBox is wrapped in a ScrolledWindow
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Rpane_fboxplotcanvas(Gtk.ScrolledWindow):
    def __init__(self):
        super(Rpane_fboxplotcanvas, self).__init__()
        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self._fb = Gtk.FlowBox()
        self._fb.set_valign(Gtk.Align.START)
        # self._fb.set_max_children_per_line(2)
        self._fb.set_min_children_per_line(2)
        self._fb.set_selection_mode(Gtk.SelectionMode.NONE)

        self.add(self._fb)
