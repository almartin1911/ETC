import serial
import sys
import glob


class ETC_Serial(serial.Serial):
    def __init__(self):
        serial.Serial.__init__(self)

    def check_connection(self):
        return True if self.is_open else False

    def open_port(self):
        if self.check_connection():
            print("Already connected")
        else:
            # Opening connection
            try:
                self.open()
                print("Connection opened")
            except Exception as e:
                    print(e)

    def close_port(self):
        if self.check_connection():
            # Closing connection
            try:
                self.close()
                print("Connection closed")
            except Exception as e:
                print(e)
        else:
            print("Nothing to disconnect")

    '''
    A fork of: https://stackoverflow.com/questions/12090503/
    listing-available-com-ports-with-python
    Original Author: https://stackoverflow.com/users/300783/thomas

    Successfully tested on:
    Windows 8.1 x64, Windows 10 x64
    Mac OS X 10.9.x / 10.10.x / 10.11.x
    Ubuntu 14.04 / 14.10 / 15.04 / 15.10 / 17.04 with both Python2 and Python3.
    '''

    def list_serial_ports(self):
        """ Lists serial port names (cross-platform)

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            # ports = glob.glob('/dev/tty[A-Za-z]*')
            # modification to show ONLY Arduinos
            ports = glob.glob('/dev/tty[A-Z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result
