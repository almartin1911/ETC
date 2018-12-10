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
        self.lbl_coords.set_text('Latitud: (Haz click derecho en el mapa)\nLongitud: (Haz click derecho en el mapa)')
        self.pack_start(self.lbl_coords, False, True, 0)

        self.btn_launch_site.set_image(launch_site_image)
        self.btn_launch_site.connect("clicked", self.on_btn_launch_site_clicked)
        self.pack_start(self.btn_launch_site, False, True, 0)

        self.grid_2nd_package = Gtk.Grid()
        self.pack_start(self.grid_2nd_package, False, True, 0)
        self.grid_2nd_package.set_column_homogeneous(True)

        v = "0"

        lbl_timer = Gtk.Label("TIMER")
        self.grid_2nd_package.attach(lbl_timer, 0, 0, 1, 1)
        self.lbl_vtimer = Gtk.Label(v)
        self.grid_2nd_package.attach(self.lbl_vtimer, 1, 0, 1, 1)

        lbl_gpsdia = Gtk.Label("DIA")
        lbl_gpsmes = Gtk.Label("MES")
        lbl_gpsanio = Gtk.Label("AÑO")
        self.grid_2nd_package.attach(lbl_gpsdia, 0, 1, 1, 1)
        self.grid_2nd_package.attach(lbl_gpsmes, 2, 1, 1, 1)
        self.grid_2nd_package.attach(lbl_gpsanio, 4, 1, 1, 1)
        self.lbl_vgpsdia = Gtk.Label(v)
        self.lbl_vgpsmes = Gtk.Label(v)
        self.lbl_vgpsanio = Gtk.Label(v)
        self.grid_2nd_package.attach(self.lbl_vgpsdia, 1, 1, 1, 1)
        self.grid_2nd_package.attach(self.lbl_vgpsmes, 3, 1, 1, 1)
        self.grid_2nd_package.attach(self.lbl_vgpsanio, 5, 1, 1, 1)

        lbl_gpshor = Gtk.Label("HORA")
        lbl_gpsmin = Gtk.Label("MIN")
        lbl_gpsseg = Gtk.Label("SEG")
        self.grid_2nd_package.attach(lbl_gpshor, 0, 2, 1, 1)
        self.grid_2nd_package.attach(lbl_gpsmin, 2, 2, 1, 1)
        self.grid_2nd_package.attach(lbl_gpsseg, 4, 2, 1, 1)
        self.lbl_vgpshor = Gtk.Label(v)
        self.lbl_vgpsmin = Gtk.Label(v)
        self.lbl_vgpsseg = Gtk.Label(v)
        self.grid_2nd_package.attach(self.lbl_vgpshor, 1, 2, 1, 1)
        self.grid_2nd_package.attach(self.lbl_vgpsmin, 3, 2, 1, 1)
        self.grid_2nd_package.attach(self.lbl_vgpsseg, 5, 2, 1, 1)

        lbl_alt1 = Gtk.Label("ALT1")
        lbl_alt2 = Gtk.Label("ALT2")
        lbl_gpsalt = Gtk.Label("ALTGPS")
        self.grid_2nd_package.attach(lbl_alt1, 0, 3, 1, 1)
        self.grid_2nd_package.attach(lbl_alt2, 1, 3, 1, 1)
        self.grid_2nd_package.attach(lbl_gpsalt, 2, 3, 1, 1)
        self.lbl_valt1 = Gtk.Label(v)
        self.lbl_valt2 = Gtk.Label(v)
        self.lbl_vgpsalt = Gtk.Label(v)
        self.grid_2nd_package.attach(self.lbl_valt1, 0, 4, 1, 1)
        self.grid_2nd_package.attach(self.lbl_valt2, 1, 4, 1, 1)
        self.grid_2nd_package.attach(self.lbl_vgpsalt, 2, 4, 1, 1)

    def on_btn_launch_site_clicked(self, button):
        self.emit('btn_launch_site_clicked')
