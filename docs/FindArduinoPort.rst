Find and setup Arduino port
===========================

Arduino boards and other USB-serial devices end up recognized as
``/dev/ttyACM*`` or ``/dev/ttyUSB*`` in your **Linux-based** host OS,
for example, ``/dev/ttyACM0``.

Communication between Arduino and PC doesn't work out of the box in
Linux (as far as I'm concerned), so, a workaround is mandatory.

Next are steps for a **first-time only setup**. However, some of these
commands might be useful if you experiencing issues with the Arduino
board connection.

On Linux
--------

#. Open a terminal and type:

   .. code:: bash

       $ ls -l /dev/ttyACM*

   With your board plugged in will tell you if it'd been recognized and
   what group(s) can access it. you should see and output similar to
   this:

   .. code:: bash

       crw-rw---- 1 root dialout 166, 0 oct 22 11:23 /dev/ttyACM0

   Note the presence of ``root`` and ``dialout`` groups. So now it's
   time to add yourself to the ``dialout`` group.

#. Add ``$YOUR_USERNAME`` to the ``dialout`` group by typing:

   .. code:: bash

       $ sudo usermod -a -G dialout $YOUR_USERNAME

#. Logout and then log back.

#. Finally, open a terminal and run ``$ groups $YOUR_USERNAME`` and look
   for ``dialout`` in the output.

**Note**: In case group change isn't recognized after the
logout/log-back step, try rebooting the system.

On Windows
----------

No special setup is required. Finding the port is really
straightforward.

#. Open **Device Manager**, and expand the ``Ports (COM & LPT)`` list.

|Serial port identification on Windows|

#. Finally, note the port number ( ``COM*``) of the Arduino board.

.. |Serial port identification on Windows| image:: https://www.mathworks.com/help/supportpkg/arduinoio/ug/win_dev_mngr_port.png

