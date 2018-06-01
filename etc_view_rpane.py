import etc_rpane_fboxplotcanvas
import etc_rpane_osmgpsmap

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class View_rpane(Gtk.Paned):
    def __init__(self):
        super(View_rpane, self).__init__()

        self.set_wide_handle(True)

        self._fboxplotcanvas = etc_rpane_fboxplotcanvas.Rpane_fboxplotcanvas()
        self.add1(self._fboxplotcanvas)
        self._osmgpsmap = etc_rpane_osmgpsmap.Rpane_osmgpsmap()
        self.add2(self._osmgpsmap)
