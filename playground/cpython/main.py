import random
import ctypes
import time

# TODO: Configure relative path.
lib = ctypes.CDLL('/home/amartin1911/dev/ETC/playground/cpython/libreria.so')


def c_add_int_array(int_array, size):
    # c_int is default restype, but let's be explicit for now
    lib.add_int_array.restype = ctypes.c_int

    # call the C function add_int_array
    sum = lib.add_int_array(int_array, size)

    return sum


def c_copy_array(chr_array_in, size, chr_array_out):
    lib.copy_array.restype = ctypes.c_void_p
    lib.copy_array(chr_array_in, size, chr_array_out)


def c_parse_package(input, size_in, output, size_out):
    lib.parse_package.restype = ctypes.c_void_p
    lib.parse_package(input, size_in, output, size_out)


def c_updateArray():
    size = 3
    array_in = (ctypes.c_int*size)(1, 2, 3)
    print("Before")
    print_array(array_in)

    lib.updateArray.restype = ctypes.c_void_p
    lib.updateArray(array_in, size)

    print("After")
    print_array(array_in)


def print_array(array):
    print(len(array), end=' | ')
    for value in array:
        print(value, end=', ')
    print()


size_a = 31
size_b = 16
# Next line generates UNIQUE random rumbers
# py_int_array = random.sample(range(0, 256), size)
# Next line generates DUPLICATE random rumbers
py_int_array = [random.choice(range(256)) for i in range(size_a)]
# print(len(py_int_array), "|", py_int_array)

# t0 = time.time()
# print(sum(py_int_array))
# t1 = time.time()

# print("Runtime: %.5f ms" % (1000 * (t1 - t0)))

# c_int_array_a = (ctypes.c_int * size_a)(*py_int_array)
# print_array(c_int_array_a)
# c_int_array_b = (ctypes.c_int * size_a)()
# print_array(c_int_array_b)

# ADD_INT_ARRAY
# t0 = time.time()
# print(c_add_int_array(c_int_array_a, size_a))
# t1 = time.time()

# print("Runtime: %.5f ms" % (1000 * (t1 - t0)))

# COPY_ARRAY
# c_copy_array(c_int_array_a, size_a, c_int_array_b)
# print_array(c_int_array_b)

# CONVIERTE
c_char_array_a = (ctypes.c_char * size_a)(*py_int_array)
print_array(c_char_array_a)
c_float_array_b = (ctypes.c_float * size_b)()
print_array(c_float_array_b)

c_parse_package(c_char_array_a, size_a, c_float_array_b, size_b)
print_array(c_float_array_b)

# c_updateArray()
