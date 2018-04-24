import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class ETC_Window(Gtk.ApplicationWindow):
    def __init__(self, app_name):
        # App data
        win_title = "ETC"
        win_subtitle = "v0.1"

        # Init window and headerbar
        Gtk.Window.__init__(self)
        self.set_title(win_title + " " + win_subtitle)
        self.set_application(app_name)

        headerbar = Gtk.HeaderBar()
        headerbar.props.show_close_button = True
        headerbar.props.title = win_title
        headerbar.props.subtitle = win_subtitle
        self.set_titlebar(headerbar)
