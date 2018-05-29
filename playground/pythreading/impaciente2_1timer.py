# https://python-para-impacientes.blogspot.com.es/2016/12/threading-programacion-con-hilos-y-ii.html
import threading
import time


def retrasado():
    nom_hilo = threading.current_thread().getName()
    contador = 1
    while(contador <= 10):
        print(f'{nom_hilo} ejecuta su trabajo {contador}')
        time.sleep(0.1)
        contador += 1
    print(f'{nom_hilo} ha terminado su trabajo')


hilo1 = threading.Timer(0.2, retrasado)
hilo1.setName('hilo1')
hilo2 = threading.Timer(0.5, retrasado)
hilo2.setName('hilo2')

hilo1.start()
hilo2.start()
print('hilo1 espera 0.2 segundos')
print('hilo2 espera 0.5 segundos')

time.sleep(0.3)
print('hilo2 va a ser cancelado')
hilo2.cancel()
print('hilo2 fue cancelado antes de iniciar su ejecucion')
