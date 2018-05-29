import threading
import time

ACTIVAS = []
NUM_DESCARGAS_SIM = 3


def descargando(semaforo, tiempo):
    global ACTIVAS
    n_hilo = threading.current_thread().name
    print(f'Esperando para descargar: {n_hilo}')

    with semaforo:
        ACTIVAS.append(n_hilo)
        print(f'Descargas activas {ACTIVAS}')
        print(f'...Descargando... {n_hilo}')
        time.sleep(tiempo)
        ACTIVAS.remove(n_hilo)
        print(f'Descarga finalizada {n_hilo}')


semaforo = threading.Semaphore(NUM_DESCARGAS_SIM)
tiempo = 3

for indice in range(1, 6):
    hilo = threading.Thread(target=descargando,
                            name='D'+str(indice),
                            args=(semaforo, tiempo))
    hilo.start()
