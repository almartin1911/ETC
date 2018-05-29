# gtk module
# import gtk
# binding for GLib
# import gobject

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gio

# matplotlib Figure object
from matplotlib.figure import Figure
# import the GtkAgg FigureCanvas object, that binds Figure to
# GTKAgg backend. In this case, this is a gtk.DrawingArea
from matplotlib.backends.backend_gtk3agg \
import FigureCanvasGTK3Agg as FigureCanvas
# needed for the sleep function
import time
# used to obtain CPU usage information
import psutil as p


def prepare_cpu_usage():
    """Helper function to return CPU usage info"""
    # get the CPU times using psutil module
    t = p.cpu_times()
    # return only the values we're interested in
    if hasattr(t, 'nice'):
        return [t.user, t.nice, t.system, t.idle]
    else:
    # special case for Windows, without 'nice' value
        return [t.user, 0, t.system, t.idle]


def get_cpu_usage():
    """Compute CPU usage comparing previous and current values"""
    # use the global 'before' variable
    global before
    # take the current CPU usage information
    now = prepare_cpu_usage()
    # compute deltas between current and previous measurements
    delta = [now[i]-before[i] for i in range(len(now))]
    # compute the total (needed for percentages calculation)
    total = sum(delta)
    # save the current measurement to before object
    before = now
    # return the percentage of CPU usage for our 4 categories
    return [(100.0*dt)/total for dt in delta]


def update_draw(*args):
    """Update the graph with current CPU usage values"""
    # use the global 'i' variable
    global i
    # get the CPU usage information
    result = get_cpu_usage()
    # append new data to the datasets
    user.append(result[0])
    nice.append(result[1])
    sys.append( result[2])
    idle.append(result[3])
    # update lines data using the lists with new data
    l_user.set_data(range(len(user)), user)
    l_nice.set_data(range(len(nice)), nice)
    l_sys.set_data( range(len(sys)), sys)
    l_idle.set_data(range(len(idle)), idle)

    # force a redraw of the Figure
    fig.canvas.draw()
    # after 30 iteration, exit; else, sleep 1 second
    i += 1
    if i > 30:
        return False
    else:
        time.sleep(1)
        return True


# global var to initialize the loop counter
i = 0
# global var, initialized with the current CPU usage values
before = prepare_cpu_usage()
# instantiate the GTK+ window object
win = Gtk.Window()
# connect the 'destroy' signal to gtk.main_quit function
win.connect("destroy", Gtk.main_quit)
# define the size of the GTK+ window
win.set_default_size(600, 400)
# set the window title
win.set_title("30 Seconds of CPU Usage Updated in real-time")
# first image setup
fig = Figure()
ax = fig.add_subplot(111)
# set specific limits for X and Y axes
ax.set_xlim(0, 30)
ax.set_ylim([0, 100])
# and disable figure-wide autoscale
ax.set_autoscale_on(False)
# generates first "empty" plots
user, nice, sys, idle = [], [], [], []
l_user, = ax.plot([], user, label='User %')
l_nice, = ax.plot([], nice, label='Nice %')
l_sys, = ax.plot([] , sys, label='Sys %')
l_idle, = ax.plot([], idle, label='Idle %')
# add legend to plot
ax.legend()
# we bind the figure to the FigureCanvas, so that it will be
# drawn using the specific backend graphic functions
canvas = FigureCanvas(fig)
# add that widget to the GTK+ main window
win.add(canvas)
# explicit update the graph (speedup graph visualization)
update_draw()
# exec our "updated" funcion when GTK+ main loop is idle
GLib.idle_add(update_draw)
# show all the widget attached to the main window
win.show_all()
# start the GTK+ main loop
Gtk.main()
