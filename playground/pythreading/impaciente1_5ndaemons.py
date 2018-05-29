import threading


def contar(numero):
    contador = 0

    while contador < 10:
        contador += 1
        print(numero, threading.get_ident(), contador)


for n_hilo in range(1, 11):
    hilo = threading.Thread(target=contar, args=(n_hilo,), daemon=True)
    hilo.start()

hilo_main = threading.main_thread()

for hilo in threading.enumerate():
    if hilo is hilo_main:
        continue

    print(hilo.getName(), hilo.ident, hilo.isDaemon(), threading.active_count())

    hilo.join()
