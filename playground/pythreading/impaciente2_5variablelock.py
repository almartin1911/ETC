import threading

TOTAL = 0


def acumula5():
    global TOTAL
    contador = 0
    hilo_actual = threading.current_thread().getName()
    num_intentos = 0

    while contador < 20:
        lo_consegui = bloquea.acquire(blocking=False)

        try:
            if lo_consegui:
                contador += 1
                TOTAL += 5
                print(f'Bloqueado por {hilo_actual}, contador {contador}')
                print(f'Total {TOTAL}')
            else:
                num_intentos += 1
                print(f'Num intentos de bloqueo: {num_intentos}.', end=' ')
                print(f'Hilo {hilo_actual} {bloquea.locked()}')
                print('Hacer otro trabajo')

        finally:
            if lo_consegui:
                print(f'Liberado bloqueo por {hilo_actual}')
                bloquea.release()


bloquea = threading.Lock()
hilo1 = threading.Thread(name='h1', target=acumula5)
hilo2 = threading.Thread(name='h2', target=acumula5)

hilo1.start()
hilo2.start()
