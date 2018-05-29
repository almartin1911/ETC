# Compare with impaciente2_4variablelock.py
import threading

TOTAL = 0


def acumula5(bloqueo):
    global TOTAL
    contador = 0
    hilo_actual = threading.current_thread().getName()

    while contador < 20:
        with bloqueo:
            contador += 1
            TOTAL += 5
            print(f'Bloqueado por {hilo_actual}, contador {contador}')
            print(f'Total {TOTAL}')

        print(f'Liberado bloqueo por {hilo_actual}')


bloqueo = threading.Lock()
hilo1 = threading.Thread(target=acumula5, args=(bloqueo,))
hilo2 = threading.Thread(target=acumula5, args=(bloqueo,))

hilo1.start()
hilo2.start()
