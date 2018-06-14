# A OsmGpsMap.Map wrapped into a Gtk.Box
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('OsmGpsMap', '1.0')

from gi.repository import Gtk, Gio, GObject
from gi.repository import OsmGpsMap as ogm


class Rpane_mapbox(Gtk.Box):
    __gsignals__ = {
        'btn_launch_site_clicked': (GObject.SIGNAL_RUN_FIRST, None, ())
    }

    def __init__(self):
        super(Rpane_mapbox, self).__init__(orientation=Gtk.Orientation.VERTICAL)

        self.map = ogm.Map()
        self.pack_start(self.map, True, True, 0)

        self.btn_launch_site = Gtk.Button()
        launch_site_icon = Gio.ThemedIcon(name="go-home-symbolic")
        launch_site_image = Gtk.Image.new_from_gicon(launch_site_icon,
                                                     Gtk.IconSize.DND)

        self.lbl_coords = Gtk.Label()
        self.lbl_coords.set_text('Latitud: (Haz click derecho)\nLongitud: (Haz click derecho)')
        self.pack_start(self.lbl_coords, False, True, 0)

        self.btn_launch_site.set_image(launch_site_image)
        self.btn_launch_site.connect("clicked", self.on_btn_launch_site_clicked)
        self.pack_start(self.btn_launch_site, False, True, 0)

        self.grid_2nd_package = Gtk.Grid()
        self.pack_start(self.grid_2nd_package, False, True, 0)
        self.grid_2nd_package.set_column_homogeneous(True)

        lbl_alt1 = Gtk.Label("ALT1")
        lbl_alt2 = Gtk.Label("ALT2")
        # lbl_alt3 = Gtk.Label("ALT3")
        lbl_timer = Gtk.Label("TIMER")
        self.grid_2nd_package.attach(lbl_alt1, 0, 0, 1, 1)
        self.grid_2nd_package.attach(lbl_alt2, 1, 0, 1, 1)
        # self.grid_2nd_package.attach(lbl_alt3, 2, 0, 1, 1)
        self.grid_2nd_package.attach(lbl_timer, 2, 0, 1, 1)

        v = "0.00"
        self.lbl_valt1 = Gtk.Label(v)
        self.lbl_valt2 = Gtk.Label(v)
        # self.lbl_valt3 = Gtk.Label(v)
        self.lbl_vtimer = Gtk.Label(v)
        self.grid_2nd_package.attach(self.lbl_valt1, 0, 1, 1, 1)
        self.grid_2nd_package.attach(self.lbl_valt2, 1, 1, 1, 1)
        # self.grid_2nd_package.attach(self.lbl_valt3, 2, 1, 1, 1)
        self.grid_2nd_package.attach(self.lbl_vtimer, 2, 1, 1, 1)

    def on_btn_launch_site_clicked(self, button):
        self.emit('btn_launch_site_clicked')
