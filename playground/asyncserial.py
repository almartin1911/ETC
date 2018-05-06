import asyncio
import serial_asyncio
import serial
import sys
import glob


class Output(asyncio.Protocol):

    header = b'\xd1'

    package = b''
    package_list = []

    package_counter = 0
    buffer_size = 32
    package_pointer = 0

    is_header = False
    first_time_header = False

    def connection_made(self, transport):
        self.transport = transport
        print('port opened', transport)
        # Manipulating Serial object via transport
        transport.serial.rts = False
        # transport.write(b'\xc2')

    def data_received(self, data):
        # # received_byte = data
        #
        # if data == self.header:
        #     if not self.first_time_header:
        #         self.is_header = True
        #         self.package_pointer = 0
        #         self.first_time_header = True
        #
        # self.package += self.data
        # self.package_pointer += 1
        #
        # if self.package_pointer >= self.buffer_size:
        #     self.package_pointer = 0
        #
        #     if self.is_header:
        #         self.package_counter += 1
        #         print(self.package_counter, self.package)
        #         self.package_list.append(self.package)
        #
        #         self.package = b''
        #
        #         self.is_header = False
        #         self.first_time_header = False
        print('data received', repr(data))
        if b'\n' in data:
            self.transport.close()

    def connection_lost(self, exc):
        print('port closed')
        self.transport.loop.stop()

    def list_serial_ports():
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


port = Output.list_serial_ports().pop()
loop = asyncio.get_event_loop()
coro = serial_asyncio.create_serial_connection(loop, Output, port,
                                               baudrate=9600)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()
