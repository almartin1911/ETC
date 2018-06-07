# import gi
# gi.require_version('Gtk', '3.0')
# from gi.repository import Gtk

import matplotlib.style
import matplotlib as mpl
mpl.use('GTK3Agg')
mpl.style.use('ggplot')
# mpl.style.use('bmh')
# mpl.style.use('fivethirtyeight')
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = 'Ubuntu'
mpl.rcParams['font.monospace'] = 'Ubuntu Mono'
mpl.rcParams['font.size'] = 10
mpl.rcParams['axes.labelsize'] = 10
# mpl.rcParams['axes.labelweight'] = 'bold'
mpl.rcParams['xtick.labelsize'] = 8
mpl.rcParams['ytick.labelsize'] = 8
mpl.rcParams['legend.fontsize'] = 10
mpl.rcParams['figure.titlesize'] = 12

from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)
from matplotlib.figure import Figure


class PlotCanvas(object):
    def __init__(self, title, label, unit, color):
        # super(PlotCanvas, self).__init__()
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)

        self.ax.set_title(title)
        self.ax.grid(True)

        self.canvas = FigureCanvas(self.fig)
        self.canvas.set_size_request(400, 300)
        self.canvas.show()

        self.data = []
        self.line, = self.ax.plot([], self.data)
        self.line.set_label(label)
        self.line.set_color(color)
        # self.ax.set_xlabel("# de Muestras")
        # self.ax.set_ylabel(f"[{unit}]")
        self.ax.legend(loc=2)

    def update_draw(self, *args):
        # print(args[0])
        self.data.append(args[0])
        # print(self.data)
        self.line.set_data(range(len(self.data)), self.data)
        # self.l_data.set_ydata(self.data)
        self.ax.relim()
        self.ax.autoscale_view(True, True, True)
        # print(self.l_data)
        try:
            self.canvas.draw()
        except Exception as e:
            print(e)
