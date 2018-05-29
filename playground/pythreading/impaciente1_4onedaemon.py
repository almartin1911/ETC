import time
import os
import threading


def chequear(nombre):
    '''Chequea tamaño de archivo'''
    contador = 0
    tam = 0

    while contador < 100:
        contador += 1
        if os.path.exists(nombre):
            estado = os.stat(nombre)
            tam = estado.st_size

        print(threading.current_thread().getName(), contador, tam, 'bytes')

        time.sleep(0.1)


def escribir(nombre):
    '''Escribe en archivo'''
    contador = 1
    while contador <= 10:
        with open(nombre, 'a') as archivo:
            archivo.write('1')
            print(threading.current_thread().getName(), contador)
            time.sleep(0.3)
            contador += 1


nombre = 'archivo.txt'
if os.path.exists(nombre):
    os.remove(nombre)

hilo_daemon = threading.Thread(name='chequear', target=chequear,
                               args=(nombre,), daemon=True)
hilo_normal = threading.Thread(name='escribir', target=escribir,
                               args=(nombre,))
hilo_daemon.start()
hilo_normal.start()

hilo_daemon.join()
print(hilo_daemon.is_alive())
