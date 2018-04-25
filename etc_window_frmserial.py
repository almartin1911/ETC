import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio


class ETC_window_frmserial(Gtk.Frame):
    def __init__(self):
        Gtk.Frame.__init__(self)
        self.set_label("Serial")

        grid = Gtk.Grid()
        self.add(grid)

        self.cbox_ports = Gtk.ComboBox()
        grid.attach(self.cbox_ports, 0, 0, 2, 1)

        btn_refresh = Gtk.Button()
        refresh_icon = Gio.ThemedIcon(name="view-refresh-symbolic")
        refresh_image = Gtk.Image.new_from_gicon(refresh_icon,
                                                 Gtk.IconSize.BUTTON)
        btn_refresh.set_image(refresh_image)
        grid.attach(btn_refresh, 2, 0, 1, 1)

        switch_serial = Gtk.Switch()
        grid.attach(switch_serial, 0, 1, 2, 1)

        btn_config = Gtk.Button()
        config_icon = Gio.ThemedIcon(name="emblem-system-symbolic")
        config_image = Gtk.Image.new_from_gicon(config_icon,
                                                Gtk.IconSize.BUTTON)
        btn_config.set_image(config_image)
        grid.attach(btn_config, 2, 1, 1, 1)
