import threading
import random
import math


def funcion1(barrera):
    n_hilo = threading.current_thread().name
    print(f'{n_hilo} esperando con {barrera.n_waiting} hilos más')

    numero = random.randint(1, 10)
    ident = barrera.wait()
    print(f'{n_hilo} ejecutando despues de la espera {ident}')
    print(f'factorial de {numero} es {math.factorial(numero)}')


NUM_HILOS = 5
barrera = threading.Barrier(NUM_HILOS)
hilos = [threading.Thread(name=f'Hilo-{i}', target=funcion1,
                          args=(barrera,)) for i in range(NUM_HILOS)]

for hilo in hilos:
    print(f'{hilo.name} comenzando ejecución')
    hilo.start()
