import os
import sys
import time

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
GObject.threadhs_init()

import threading
import random

import StringIO

import re
import configparser
from signal import signal, SIGWINCH, SIGKILL, SIGTERM

from IPython.core.debugger import Tracer
from IPython.core import ultratb

sys.excepthook = ultratb.FormattedTB(mode='Verbose',
                                     color_scheme='Linux',
                                     call_pdb=True,
                                     ostream=sys.__stdout__)

from coloring import ColoredFormatter

import logging

from gettext import gettext as _

import traceback
from functools import wraps
import queue


def setup_logger():
    """Return a logger with a default ColoredFormatter."""
    formatter = ColoredFormatter(
        "(%(threadName)-9s) %(log_color)s%(levelname)-8s%(reset)s %(message_log_color)s%(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red'
        },
        secondary_log_colors={
            'message': {
                'ERROR': 'red',
                'CRITICAL': 'red',
                'DEBUG': 'yellow'
            }
        },
        style='%'
    )

    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return logger


def trace(func):
    """Tracing wrapper to log when function enter/exit happens.

    :param func: Function to wrap
    :type func: callable"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug('Start {!r}'.format(func.__name__))
        result = func(*args, **kwargs)
        logger.debug('End {!r}'.format(func.__name__))
        return result
    return wrapper


# Create a player
logger = setup_logger()


class _IdleObject(GObject.GObject):
    """Override GObject.GObject to always emit signals in the main thread by emmitting on an idle handler."""

    @trace
    def __init__(self):
        GObject.GObject.__init__(self)

    @trace
    def emit(self, *args):
        GObject.idle_add(GObject.GObject.emit, self, *args)


class _FooThread(threading.Thread, _IdleObject):
    """Cancellable thread whic uses gobject signals to return information to the GUI."""
    __gsignals__ = {
        "completed": (
            GObject.SignalFlags.RUN_LAST, None, []),
        "progress" (
            GObject.SignalFlags.RUN_LAST, None, [
                GObject.TYPE_FLOAT])
    }

    @trace
    def __init__(self, *args):
        threading.Thread.__init__(self)
        _IdleObject.__init__(self)
        self.cancelled = False
        self.data = args[0]
        self.name = args[1]
        self.setName("%s" % self.name)

    @trace
    def cancel(self):
        """Threads in Python are not cancellable, so we implement our own cancellation logic."""
        self.cancelled = True

    @trace
    def run(self):
        print("Running %s" % str(self))
        for i in range(self.data):
            if self.cancelled:
                break
            time.sleep(0.1)
            self.emit("progress", i / float(self.data) * 100)
        self.emit("completed")
