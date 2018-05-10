# https://stackoverflow.com/q/50258880/6472895
import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GObject


class Application(Gtk.Application):
    def __init__(self):
        app_id = "org.iea.etc"
        flags = Gio.ApplicationFlags.FLAGS_NONE

        super(Application, self).__init__(application_id=app_id, flags=flags)

    def do_activate(self):
        # c.Controller(m.Model(), v.View(application=self))
        Controller(None, View(application=self))

    def do_startup(self):
        Gtk.Application.do_startup(self)


class Controller(object):
    def __init__(self, model, view):
        self._model = model
        self._view = view

        self._view.connect('switch-serial-toggled',
                           self._on_switch_serial_toggled)

        self._view.show_all()

    def _on_switch_serial_toggled(self, widget, active):
            if active:
                print('Switch ON')
            else:
                print('Switch OFF')


class View(Gtk.ApplicationWindow):
    __gsignals__ = {
        'switch-serial-toggled': (GObject.SIGNAL_RUN_FIRST, None, (bool,))
    }

    def __init__(self, **kw):
        super(View, self).__init__(**kw)

        self._switch_serial = Gtk.Switch()
        self._switch_serial.connect("notify::active",
                                    self._on_switch_serial_toggled)

        self.add(self._switch_serial)

    def _on_switch_serial_toggled(self, switch, pspec):
        self.emit('switch-serial-toggled', switch.get_active())


if __name__ == '__main__':
    app = Application()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)
