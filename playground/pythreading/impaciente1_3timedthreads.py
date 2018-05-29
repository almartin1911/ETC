import time
import threading

vmax_hilos = {}


def contar(segundos):
    '''Contar hasta un límite de tiempo'''
    global vmax_hilos
    contador = 0
    tinicio = time.time()
    tlimite = tinicio + segundos
    nombre = threading.current_thread().getName()

    while tinicio <= tlimite:
        contador += 1
        print(nombre, contador)

        tinicio = time.time()

    vmax_hilos[nombre] = contador
    if threading.active_count() == 2:
        print(vmax_hilos)
        print(threading.enumerate())


seg = 0.001
for n_hilo in range(5):
    hilo = threading.Thread(name=f'hilo {n_hilo}', target=contar, args=(seg,))
    hilo.start()
