import gi

gi.require_version('Gtk', '3.0')
gi.require_version('OsmGpsMap', '1.0')

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import OsmGpsMap as osmgpsmap
from gi.repository import GObject

# Deprecated since PyGObject v3.11
# GObject.threads_init()
# Gdk.threads_init()

print ("using library: %s (version %s)" % (osmgpsmap.__file__, osmgpsmap._version))

assert osmgpsmap._version == "1.0"


class DummyMapNoGpsPoint(osmgpsmap.Map):
    def do_draw_gps_point(self, drawable):
        pass


GObject.type_register(DummyMapNoGpsPoint)


class DummyLayer(GObject.GObject, osmgpsmap.MapLayer):
    def __init__(self):
        GObject.GObject.__init__(self)

    def do_draw(self, gpsmap, gdkdrawable):
        pass

    def do_render(self, gpsmap):
        pass

    def do_busy(self):
        return False

    def do_button_press(self, gpsmap, gdkeventbutton):
        return False


GObject.type_register(DummyLayer)


class UI(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, type=Gtk.WindowType.TOPLEVEL)

        self.connect('destroy', lambda x: Gtk.main_quit())
        self.set_default_size(500, 500)
        self.set_title('osmgpsmap tests')

        self.vbox = Gtk.VBox(False, 0)
        self.add(self.vbox)

        if 0:
            self.osm = DummyMapNoGpsPoint()
        else:
            self.osm = osmgpsmap.Map()

        self.osm.layer_add(
            osmgpsmap.MapOsd(
                show_dpad=True,
                show_zoom=True,
                show_crosshair=True,
                show_coordinates=True,
                show_scale=True
            )
        )

        self.osm.layer_add(
            DummyLayer()
        )

        self.vbox.pack_start(self.osm, True, True, 0)

        #btn_home = Gtk.Button(stock=Gtk.STOCK_HOME)
        #btn_home.connect('clicked', self.on_btn_home_clicked)

        punto_pucarani = [-16.411514, -68.487633]
        punto_cota_cota = [-16.538275, -68.069592]


window = UI()
window.show_all()
Gtk.main()
