# TODO: On linux: sudo usermod -a -G dialout $USER
import serial
import sys
import glob


class Serial(serial.Serial):
    def __init__(self, **kw):
        super(Serial, self).__init__(**kw)

    def open_port(self):
        if self.is_open:
            print("Already connected")
        else:
            # Opening connection
            try:
                self.open()
                print("Connection opened")
                print(self)
            except Exception as e:
                    print(e)

    def close_port(self):
        if self.is_open:
            # Closing connection
            try:
                self.close()
                print("Connection closed")
                print(self)
            except Exception as e:
                print(e)
        else:
            print("Nothing to disconnect")

    # fork of:
    # https://stackoverflow.com/questions/12090503/listing-available-com-ports
    # -with-python

    def list_serial_ports(self):
        """ Lists serial port names (cross-platform)

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or \
                sys.platform.startswith('cygwin'):
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
