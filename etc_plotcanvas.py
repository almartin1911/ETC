import matplotlib as mpl
mpl.use('GTK3Agg')

from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)
from matplotlib.figure import Figure


class PlotCanvas(object):
    def __init__(self, **kw):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.legend()
        self.ax.grid(True)

        self.canvas = FigureCanvas(self.fig)
        self.canvas.set_size_request(400, 200)

        self.data = []
        self.line, = self.ax.plot([], self.data)
        self.line.set_label("LabelTest")

    def update_draw(self, *args):
        # print(args[0])
        self.data.append(args[0])
        # print(self.data)
        self.l_data.set_data(range(len(self.data)), self.data)
        # self.l_data.set_ydata(self.data)
        self.ax.relim()
        self.ax.autoscale_view(True, True, True)
        # print(self.l_data)
        try:
            self.canvas.draw()
        except Exception as e:
            print(e)
