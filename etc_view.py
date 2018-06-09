import etc_view_lpane
import etc_view_rpane

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

settings = Gtk.Settings.get_default()
settings.set_property("gtk-theme-name", "Adwaita")
# settings.set_property("gtk-theme-name", "Adwaita-dark")


class View(Gtk.ApplicationWindow):
    def __init__(self, **kw):
        # App data
        win_title = "Estación Terrena Chitisat"
        win_subtitle = "v0.4.6"

        # Init window and headerbar
        super(View, self).__init__(**kw)
        self.set_title(win_title + " " + win_subtitle)
        self._headerbar = Gtk.HeaderBar()
        self._headerbar.props.show_close_button = True
        self._headerbar.props.title = win_title
        self._headerbar.props.subtitle = win_subtitle
        self.set_titlebar(self._headerbar)

        # Setting up the style from a css file
        self._css_provider = Gtk.CssProvider()
        self._css_provider.load_from_path("style.css")
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            self._css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # A Gtk.Grid as main container
        self._grid = Gtk.Grid()
        # Adding grid to window
        self.add(self._grid)

        # TODO: An interactive Infobar
        # A Gtk.InfoBar as top statusbar
        self._infobar = Gtk.InfoBar()
        self._infobar.set_message_type(Gtk.MessageType.INFO)
        infobar_label = Gtk.Label("Barra de estado")
        infobar_content = self._infobar.get_content_area()
        infobar_content.add(infobar_label)
        # Attaching _infobar to grid
        self._grid.attach(self._infobar, 0, 0, 1, 1)

        # An horizontal Gtk.Paned as secondary container
        self._hpaned = Gtk.Paned()
        # self._hpaned.set_wide_handle(True)
        # Attaching self._hpaned to grid
        self._grid.attach(self._hpaned, 0, 1, 1, 1)
        # Adding panes to self._hpaned
        self._lpane = etc_view_lpane.View_lpane()
        self._hpaned.add1(self._lpane)
        self._rpane = etc_view_rpane.View_rpane()
        self._hpaned.add2(self._rpane)

        # Misc window settings
        self.maximize()
