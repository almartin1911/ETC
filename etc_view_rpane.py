import etc_rpane_plotting

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class View_rpane(Gtk.Grid):
    def __init__(self):
        super(View_rpane, self).__init__()

        self._plotting = etc_rpane_plotting.Rpane_plotting()
        self.attach(self._plotting, 0, 0, 1, 1)
