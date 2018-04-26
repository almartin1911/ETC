import etc_window_frmserial as frmserial
import etc_window_frmparameters as frmparameters
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class ETC_Window_lpane(Gtk.Grid):
    def __init__(self, controller):
        Gtk.Grid.__init__(self)

        frame_serial = frmserial.ETC_window_frmserial(controller)
        self.attach(frame_serial, 0, 0, 1, 1)

        frame_parameters = frmparameters.ETC_window_frmparameters(controller)
        self.attach(frame_parameters, 0, 1, 1, 1)
