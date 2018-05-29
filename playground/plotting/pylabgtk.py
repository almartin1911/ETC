# https://matplotlib.org/gallery/user_interfaces/pylab_with_gtk_sgskip.html
# Doesn't work on GTK3
from __future__ import print_function
import matplotlib
matplotlib.use('GTKAgg')
import matplotlib.pyplot as plt


fig, ax = plt.subplots()
plt.plot([1, 2, 3], 'ro-', label='easy as 1 2 3')
plt.plot([1, 4, 9], 'gs--', label='easy as 1 2 3 squared')
plt.legend()


manager = plt.get_current_fig_manager()
# you can also access the window or vbox attributes this way
toolbar = manager.toolbar

# now let's add a button to the toolbar
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

next = 8  # where to insert this in the mpl toolbar
button = Gtk.Button('Click me')
button.show()


def clicked(button):
    print('hi mom')
button.connect('clicked', clicked)

toolitem = Gtk.ToolItem()
toolitem.show()
toolitem.set_tooltip(
    toolbar.tooltips,
    'Click me for fun and profit')

toolitem.add(button)
toolbar.insert(toolitem, next)
next += 1

# now let's add a widget to the vbox
label = Gtk.Label()
label.set_markup('Drag mouse over axes for position')
label.show()
vbox = manager.vbox
vbox.pack_start(label, False, False)
vbox.reorder_child(manager.toolbar, -1)


def update(event):
    if event.xdata is None:
        label.set_markup('Drag mouse over axes for position')
    else:
        label.set_markup('<span color="#ef0000">x,y=(%f, %f)</span>' % (event.xdata, event.ydata))

plt.connect('motion_notify_event', update)

plt.show()
