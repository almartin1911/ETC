# NOTE: Needs an Arduino program which sends "package_size" sized data
# with a "header" header.
# ls /dev/tty*

import serial
import sys
import time
import bitstring
import numpy

port = '/dev/ttyACM0'
arduino = serial.Serial(port, 9600)
time.sleep(2)
command1 = b'\xc2'
command2 = b'\xc3'

# arduino.write(command2)

header = b'\xd1'
package_size = 31

# package = bytearray()
package = numpy.empty(dtype=numpy.uint8, shape=package_size)

package_counter = 0
package_pointer = 0

is_header = False
first_time_header = False

while True:
    # while arduino.in_waiting > 0: BUG: CAUSES 100% CPU CONSUMPTION
    received_byte = arduino.read()
    print(package_pointer, received_byte, end=", ")

    if received_byte == header:
        if not first_time_header:
            is_header = True
            package_pointer = 0
            first_time_header = True
            # package = bytearray()

    int_received_byte = int.from_bytes(received_byte, byteorder=sys.byteorder)
    # package.append(int_received_byte)
    package[package_pointer] = int_received_byte
    package_pointer += 1

    if package_pointer >= package_size:
        package_pointer = 0

        if is_header:
            bitstream_package = bitstring.BitStream(package.tobytes())
            package_counter += 1
            # print(package_counter, package)
            print('#', package_counter, ':', bitstream_package,
                  len(bitstream_package))

            is_header = False
            first_time_header = False

# return package_list
