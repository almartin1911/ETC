# Based on matplotlib.gtk

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import matplotlib as mpl
mpl.use('GTK3Agg')
from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)
from matplotlib.figure import Figure
# import numpy as np


class Rpane_plotting(Gtk.Box):
    def __init__(self):
        super(Rpane_plotting, self).__init__()
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)

        self.ax.set_xlim(0, 100)
        self.ax.set_ylim([0, 255])

        # self.ax.set_autoscale_on(False)

        self.data = []
        self.l_data, = self.ax.plot([], self.data, label='MagY')
        self.ax.legend()
        self.ax.grid()

        self.canvas = FigureCanvas(self.fig)
        self.canvas.set_size_request(800, 600)
        self.canvas.show()

        # self.update_draw(128)
        # self.attach(canvas, 0, 0, 1, 1)
        self.pack_start(self.canvas, True, True, 0)

    def update_draw(self, *args):
        # print(args[0])
        self.data.append(args[0])
        # print(self.data)
        self.l_data.set_data(range(len(self.data)), self.data)
        # print(self.l_data)
        try:
            self.canvas.draw()
        except Exception as e:
            print(e)
