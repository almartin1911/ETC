import ctypes
import random
import bitstring

size_s = 31
s = bytearray(random.choice(range(256)) for i in range(size_s))
# for value in range(65, 100):
#     s.append(value)
print(s, len(s))
bs = bitstring.BitStream(s)
bs.pos = 0
while(bs.pos < len(bs)):
    number = bs.read(8).uint
    print(f'Pos: {bs.pos} - BytePos: {bs.bytepos} - Number: {number}')

c_char_array = (ctypes.c_char * len(s))(*s)
c_char_array
c_char_array.value
len(c_char_array)
type(c_char_array)
c_char_array._type_

size = 16
c_float_array = (ctypes.c_float * size)()
c_float_array
len(c_float_array)
type(c_float_array)
c_float_array._type_

lib = ctypes.CDLL('/home/amartin1911/dev/ETC/playground/cpython/libreria.so')


def c_convierte(input, size_in, output, size_out):
    lib.convierte.restype = ctypes.c_void_p
    lib.convierte(input, size_in, output, size_out)


def print_array(array):
    print(len(array), end=' | ')
    for value in array:
        print(value, end=', ')
    print()


print_array(c_char_array)
print_array(c_float_array)

c_convierte(c_char_array, len(c_char_array), c_float_array, len(c_float_array))
print_array(c_float_array)
py_list = []

for value in c_float_array:
    py_list.append(value)

py_list

len(py_list)
