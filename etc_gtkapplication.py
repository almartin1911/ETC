import etc_model as model
import etc_view as view
import etc_controller as controller

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio


class Application(Gtk.Application):
    def __init__(self):
        app_id = "org.iea.etc"
        flags = Gio.ApplicationFlags.FLAGS_NONE

        super(Application, self).__init__(application_id=app_id, flags=flags)

    def do_activate(self):
        controller.Controller(model, view.View(application=self))

    def do_startup(self):
        Gtk.Application.do_startup(self)
