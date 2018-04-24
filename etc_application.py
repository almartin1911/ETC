import etc_window as view
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio


class ETC_Application(Gtk.Application):
    def __init__(self):
        application_id = "org.iea.etc"
        flags = Gio.ApplicationFlags.FLAGS_NONE

        Gtk.Application.__init__(self, application_id=application_id,
                                 flags=flags)

    def do_activate(self):
        main_window = view.ETC_Window(self)
        main_window.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)
