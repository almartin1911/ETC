import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject


class View(Gtk.ApplicationWindow):
    BUTTON_PAGE = 'button'
    GREETING_PAGE = 'greeting'

    __gsignals__ = {
        'button-clicked': (GObject.SIGNAL_RUN_FIRST, None, ())
    }

    def __init__(self, **kw):
        super(View, self).__init__(**kw)

        self._grid = Gtk.Grid(vexpand=True)
        self.add(self._grid)

        self._stack = Gtk.Stack(
            transition_duration=500,
            transition_type=Gtk.StackTransitionType.CROSSFADE
        )

        self._button = Gtk.Button(label='Click me')
        self._button.connect('clicked', self._on_clicked)
        self._stack.add_titled(self._button, self.BUTTON_PAGE,
                               self.BUTTON_PAGE)

        self._label = Gtk.Label()
        self._stack.add_titled(self._label, self.GREETING_PAGE,
                               self.GREETING_PAGE)
        # self.add(self._stack)

        self._stack_switcher = Gtk.StackSwitcher()
        self._stack_switcher.set_stack(self._stack)

        self._grid.attach(self._stack_switcher, 0, 0, 1, 1)
        self._grid.attach(self._stack, 0, 1, 1, 1)

    def _on_clicked(self, button, *args):
        self.emit('button-clicked')

    def change_page(self, page):
        self._stack.props.visible_child_name = page

    def set_text(self, text):
        self._label.props.label = text
