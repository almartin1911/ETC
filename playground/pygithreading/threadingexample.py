import threading
import time

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk


class Window(Gtk.Window):
    def __init__(self):
        super(Window, self).__init__()
        self.connect("destroy", Gtk.main_quit)
        self.set_default_size(400, 200)

        self.progress = Gtk.ProgressBar(show_text=True)
        self.add(self.progress)

        thread = threading.Thread(target=self.example_target)
        thread.daemon = True
        thread.start()

    def update_progress(self, i):
        self.progress.pulse()
        self.progress.set_text(str(i))
        return False

    def example_target(self):
        for i in range(50):
            GLib.idle_add(self.update_progress, i)
            time.sleep(0.2)

win = Window()
win.show_all()
Gtk.main()
