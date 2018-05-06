import serial
import time

port = '/dev/ttyACM0'
arduino = serial.Serial(port, 9600)
time.sleep(2)
command1 = b'\xc2'
command2 = b'\xc3'

#arduino.write(command2)

header = b'\xd1'

package = bytearray()
package_list = []

package_counter = 0
buffer_size = 32
package_pointer = 0

is_header = False
first_time_header = False

while True:
    # while arduino.in_waiting > 0: CAUSES 100% CPU
    received_byte = arduino.read()
    print(package_pointer, received_byte, end=", ")

    if received_byte == header:
        if not first_time_header:
            is_header = True
            package_pointer = 0
            first_time_header = True

    package[package_pointer] = int(received_byte, 16)
    package_pointer += 1

    if package_pointer >= buffer_size:
        package_pointer = 0

        if is_header:
            package_counter += 1
            print(package_counter, package)
            package_list.append(package)

            is_header = False
            first_time_header = False

# return package_list
