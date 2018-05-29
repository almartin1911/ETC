import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import matplotlib as mpl
mpl.use('GTK3Agg')
from matplotlib.backends.backend_gtk3agg \
    import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.backends.backend_gtk3 \
    import NavigationToolbar2GTK3 as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np


class MyWindow(Gtk.Window):
    def __init__(self):
        super(MyWindow, self).__init__()
        # self.set_default_size(800, 600)
        self.set_title("Embedding matplotlib in Gtk+3")
        self.connect("destroy", Gtk.main_quit)

        self.grid = Gtk.Grid()
        self.add(self.grid)

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.build_figure()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.set_size_request(800, 600)
        # self.canvas.show()
        self.grid.attach(self.canvas, 0, 0, 1, 1)

        self.toolbar = NavigationToolbar(self.canvas, self)
        self.grid.attach(self.toolbar, 0, 1, 1, 1)

    def build_figure(self):
        ax = self.fig.add_subplot(111)
        x = np.arange(0, 2*np.pi, .01)
        y = np.sin(x**2)*np.exp(-x)
        ax.plot(x, y)


win = MyWindow()
win.show_all()
Gtk.main()
