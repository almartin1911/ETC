import etc_window_lpane as lpane
import etc_window_rpane as rpane
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class ETC_Window(Gtk.ApplicationWindow):
    def __init__(self, app_name, controller):
        # App data
        win_title = "ETC"
        win_subtitle = "v0.2.5"

        # Init window and headerbar
        Gtk.Window.__init__(self)
        self.set_title(win_title + " " + win_subtitle)
        self.set_application(app_name)
        headerbar = Gtk.HeaderBar()
        headerbar.props.show_close_button = True
        headerbar.props.title = win_title
        headerbar.props.subtitle = win_subtitle
        self.set_titlebar(headerbar)

        # Setting up the style from a css file
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("style.css")
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # A Gtk.Grid as main container
        grid = Gtk.Grid()
        # Adding grid to window
        self.add(grid)

        # A Gtk.InfoBar as top statusbar
        self.infobar = Gtk.InfoBar()
        self.infobar.set_message_type(Gtk.MessageType.WARNING)
        infobar_label = Gtk.Label("Barra de estado")
        infobar_content = self.infobar.get_content_area()
        infobar_content.add(infobar_label)
        # Attaching infobar to grid
        grid.attach(self.infobar, 0, 0, 1, 1)

        # A Gtk.Paned horizontally as secondary container
        hpaned = Gtk.Paned()
        hpaned.set_wide_handle(True)
        # Attaching hpaned to grid
        grid.attach(hpaned, 0, 1, 1, 1)
        # Adding panes to hpaned
        hpaned.add1(lpane.ETC_Window_lpane(controller))
        hpaned.add2(rpane.ETC_Window_rpane())
