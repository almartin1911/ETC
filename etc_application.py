import etc_window
import etc_controller
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
        controller = etc_controller.ETC_controller()
        view = etc_window.ETC_Window(app_name=self, controller=controller)
        view.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)
