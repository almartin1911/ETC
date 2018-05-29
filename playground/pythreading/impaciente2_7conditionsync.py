import threading
import random
import math
import time

LISTA = []


def funcion1(condicion):
    global LISTA
    n_hilo = threading.current_thread().name
    print(f'{n_hilo} esperando a que se generen los números')

    with condicion:
        condicion.wait()
        print('Elementos:', len(LISTA))
        print('Suma total:', math.fsum(LISTA))


def funcion2(condicion):
    global LISTA
    n_hilo = threading.current_thread().name
    print(f'{n_hilo} generando números')

    with condicion:
        for numeros in range(1, 1001):
            entero = random.randint(1, 100)
            LISTA.append(entero)
        print('Ya hay 1000 números')
        condicion.notifyAll()


condicion = threading.Condition()
hilo1 = threading.Thread(target=funcion1, args=(condicion,))
hilo2 = threading.Thread(target=funcion2, args=(condicion,))

hilo1.start()
hilo2.start()
