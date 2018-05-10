import ctypes

library = ctypes.CDLL('./library.so')

number = 5
if library.evenOrOdd(number) is 1:
    print(f'{number} es PAR')
else:
    print(f'{number} es IMPAR')

number = 6
if library.evenOrOdd(number) is 1:
    print(f'{number} es PAR')
else:
    print(f'{number} es IMPAR')
