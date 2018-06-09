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
        self.lbl_coords.set_text('Latitud: - \nLongitud: -')
        self.pack_start(self.lbl_coords, False, True, 0)

        self.btn_launch_site.set_image(launch_site_image)
        self.btn_launch_site.connect("clicked", self.on_btn_launch_site_clicked)
        self.pack_start(self.btn_launch_site, False, True, 0)

    def on_btn_launch_site_clicked(self, button):
        self.emit('btn_launch_site_clicked')
