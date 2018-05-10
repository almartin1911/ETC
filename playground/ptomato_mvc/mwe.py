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

        self._view.connect('notify::active',
                           self._on_switch_serial_toggled)

        self._view.show_all()

    def _on_switch_serial_toggled(self, switch, state):
            if self._view._switch_serial.get_active():
                print('Switch ON')
            else:
                print('Switch OFF')


class View(Gtk.ApplicationWindow):
    __gsignals__ = {
        'notify::active': (GObject.SIGNAL_RUN_FIRST, None, ())
    }

    def __init__(self, **kw):
        super(View, self).__init__(**kw)

        self._switch_serial = Gtk.Switch()
        self._switch_serial.connect("notify::active",
                                    self.on_switch_serial_toggled)

        self.add(self._switch_serial)

    def on_switch_serial_toggled(self, switch, state):
        self.emit('notify::active', state)


if __name__ == '__main__':
    app = Application()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)
