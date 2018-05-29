import sys
import time
import psutil

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gio

import matplotlib as mpl
mpl.use('GTK3Agg')
from matplotlib.backends.backend_gtk3agg \
    import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.figure import Figure


class Application(Gtk.Application):
    def __init__(self):
        app_id = "org.iea.example"
        flags = Gio.ApplicationFlags.FLAGS_NONE

        super(Application, self).__init__(application_id=app_id, flags=flags)

    def do_activate(self):
        window = PlotterWindow(application=self)
        window.show_all()


class PlotterWindow(Gtk.ApplicationWindow):
    def __init__(self, **kw):
        super(PlotterWindow, self).__init__(**kw)
        self.set_title("Real-time plotting")
        self.set_default_size(600, 400)
        # self.grid = Gtk.Grid()
        # self.add(self.grid)

        self.i = 0
        self.before = self.prepare_cpu_usage()

        self.fig = Figure()
        ax = self.fig.add_subplot(111)

        ax.set_xlim(0, 30)
        ax.set_ylim([0, 100])

        ax.set_autoscale_on(False)

        self.user, self.nice, self.sys, self.idle = [], [], [], []
        self.l_user, = ax.plot([], self.user, label='User %')
        self.l_nice, = ax.plot([], self.nice, label='Nice %')
        self.l_sys, = ax.plot([], self.sys, label='Sys %')
        self.l_idle, = ax.plot([], self.idle, label='Idle %')

        ax.legend()
        self.canvas = FigureCanvas(self.fig)
        self.add(self.canvas)

        self.update_draw()

        GLib.idle_add(self.update_draw)

    def prepare_cpu_usage(self):
        t = psutil.cpu_times()
        if hasattr(t, 'nice'):
            return [t.user, t.nice, t.system, t.idle]
        else:
            return [t.user, 0, t.system, t.idle]

    def get_cpu_usage(self):
        now = self.prepare_cpu_usage()
        delta = [now[i]-self.before[i] for i in range(len(now))]
        total = sum(delta)

        self.before = now

        return [(100.0*dt)/total for dt in delta]

    def update_draw(self, *args):
        result = self.get_cpu_usage()
        self.user.append(result[0])
        self.nice.append(result[1])
        self.sys.append(result[2])
        self.idle.append(result[3])

        self.l_user.set_data(range(len(self.user)), self.user)
        self.l_nice.set_data(range(len(self.nice)), self.nice)
        self.l_sys.set_data(range(len(self.sys)), self.sys)
        self.l_idle.set_data(range(len(self.idle)), self.idle)

        self.fig.canvas.draw()

        self.i += 1
        if self.i > 30:
            return False
        else:
            time.sleep(1)

        return True


def main():
    app = Application()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)


if __name__ == '__main__':
    main()
