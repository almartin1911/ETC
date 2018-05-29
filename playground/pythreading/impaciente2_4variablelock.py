import threading

TOTAL = 0


def acumula5():
    global TOTAL
    contador = 0
    hilo_actual = threading.current_thread().getName()

    while contador < 20:
        print(f'Esperando para bloquear {hilo_actual}')
        bloquea.acquire()

        try:
            contador += 1
            TOTAL += 5
            print(f'Bloqueado por {hilo_actual}, contador {contador}')
            print(f'Total {TOTAL}')

        finally:
            print(f'Liberado bloqueo por {hilo_actual}')
            bloquea.release()


bloquea = threading.Lock()
hilo1 = threading.Thread(name='h1', target=acumula5)
hilo2 = threading.Thread(name='h2', target=acumula5)

hilo1.start()
hilo2.start()
