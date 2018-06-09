import gi

gi.require_version('Gtk', '3.0')
gi.require_version('OsmGpsMap', '1.0')

from gi.repository import Gtk
from gi.repository import OsmGpsMap as ogm


class Rpane_osmgpsmap(Gtk.Box):
    def __init__(self):
        super(Rpane_osmgpsmap, self).__init__(orientation=Gtk.Orientation.VERTICAL)
        punto_cota_cota = [-16.538275, -68.069592]

        self.map = ogm.Map()
        self.pack_start(self.map, True, True, 0)

        self.layer_osd = ogm.MapOsd(show_dpad=True,
                                    show_zoom=True,
                                    show_crosshair=True,
                                    show_coordinates=True,
                                    show_scale=True)
        self.map.layer_add(self.layer_osd)
        max_zoom, min_zoom = self.map.props.max_zoom, self.map.props.min_zoom
        # print(max_zoom, min_zoom)
        self.map.set_center_and_zoom(punto_cota_cota[0], punto_cota_cota[1], max_zoom)

        self.map_track = ogm.MapTrack()

        self.point = ogm.MapPoint()
        self.point.set_degrees(punto_cota_cota[0], punto_cota_cota[1])
        self.map_track.add_point(self.point)

        # print(self.map_track.get_points())

        self.map.track_add(self.map_track)
        # self.box.pack_start(self.map_track, True, True, 0)

        # self.grid = Gtk.Grid()
        # self.box.pack_start(self.grid, True, True, 0)

        self.lbl_coords = Gtk.Label("Coordenadas")
        self.pack_start(self.lbl_coords, False, True, 0)
