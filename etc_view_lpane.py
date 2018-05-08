import etc_lpane_frameserial
import etc_lpane_frameparameters
import etc_lpane_framecommands

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class View_lpane(Gtk.Grid):
    def __init__(self):
        super(View_lpane, self).__init__()

        self._frame_serial = etc_lpane_frameserial.Lpane_frameserial()
        self.attach(self._frame_serial, 0, 0, 1, 1)

        # frame_parameters = frmparameters.ETC_window_frmparameters(controller)
        # self.attach(frame_parameters, 0, 1, 1, 1)
        #
        # frame_commands = frmcommands.ETC_window_frmcommands(controller)
        # self.attach(frame_commands, 0, 2, 1, 1)
