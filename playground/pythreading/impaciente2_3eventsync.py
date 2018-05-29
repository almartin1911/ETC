import threading


def avanza(evento):
    ciclo = 0
    valor = 0

    while valor < 20:
        estado = evento.wait()

        if estado:
            ciclo += 1
            valor += 1
            print('avanza', valor)

            if ciclo == 10 and hilo2.isAlive():
                evento.clear()
                ciclo = 0
    print('avanza: ha finalizado')


def retrocede(evento, tiempo):
    ciclo = 0
    valor = 21

    while valor > 1:
        estado = evento.wait(tiempo)

        if not estado:
            ciclo += 1
            valor -= 1
            print('retrocede', valor)

            if ciclo == 5 and hilo1.isAlive():
                evento.set()
                ciclo = 0
    print('retrocede: ha finalizado')


evento = threading.Event()
hilo1 = threading.Thread(target=avanza, args=(evento,))
hilo2 = threading.Thread(target=retrocede, args=(evento, 0.5))

hilo1.start()
hilo2.start()
