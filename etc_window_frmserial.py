import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio


class ETC_window_frmserial(Gtk.Frame):
    def __init__(self, controller):
        Gtk.Frame.__init__(self)
        self.set_label("Conexión Serial")

        self.controller = controller

        grid = Gtk.Grid()
        self.add(grid)

        self.cbox_ports = Gtk.ComboBox()
        renderer_text = Gtk.CellRendererText()
        self.cbox_ports.pack_start(renderer_text, True)
        self.cbox_ports.add_attribute(renderer_text, "text", 0)
        self.controller.load_ports(self.cbox_ports)
        self.cbox_ports.connect("changed", self.on_cbox_ports_changed)
        grid.attach(self.cbox_ports, 0, 0, 2, 1)

        btn_refresh = Gtk.Button()
        refresh_icon = Gio.ThemedIcon(name="view-refresh-symbolic")
        refresh_image = Gtk.Image.new_from_gicon(refresh_icon,
                                                 Gtk.IconSize.BUTTON)
        btn_refresh.set_image(refresh_image)
        btn_refresh.connect("clicked", self.on_btn_refresh_clicked)
        grid.attach(btn_refresh, 2, 0, 1, 1)

        switch_serial = Gtk.Switch()
        switch_serial.connect("notify::active", self.on_switch_serial_toggled)
        grid.attach(switch_serial, 0, 1, 2, 1)

        btn_config = Gtk.Button()
        config_icon = Gio.ThemedIcon(name="emblem-system-symbolic")
        config_image = Gtk.Image.new_from_gicon(config_icon,
                                                Gtk.IconSize.BUTTON)
        btn_config.set_image(config_image)
        grid.attach(btn_config, 2, 1, 1, 1)

    def on_cbox_ports_changed(self, cbox):
        self.controller.set_port(cbox)

    def on_btn_refresh_clicked(self, button):
        self.controller.load_ports(self.cbox_ports)
        print('Refresh clicked!')

    def on_switch_serial_toggled(self, switch, state):
        if switch.get_active():
            print('Switch ON')
            self.controller.arduino.open_port()
            # controller.start_read_thread(self.arduino,
            #                              self.tree_view_parameters)
            print(self.controller.arduino)
        else:
            print('Switch OFF')
            self.controller.arduino.close_port()
            print(self.controller.arduino)
