# https://python-para-impacientes.blogspot.com/2016/12/threading-programacion-con-hilos-i.html
import threading


def contar():
    '''Contar hasta cien'''
    contador = 0
    while contador < 100:
        contador += 1
        print('Hilo:',
              threading.current_thread().getName(),
              'con identificador:',
              threading.current_thread().ident,
              'Contador:', contador)


NUM_HILOS = 3

for n_hilo in range(NUM_HILOS):
    # hilo = threading.Thread(name=f'hilo {n_hilo}', target=contar)
    hilo = threading.Thread(target=contar)
    hilo.start()
