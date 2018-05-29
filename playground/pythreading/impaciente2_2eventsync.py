import threading
import random


def gen_pares():
    num_pares = 0
    print('Numeros:', end=' ')
    while num_pares < 25:
        numero = random.randint(1, 10)
        resto = numero % 2
        if resto == 0:
            num_pares += 1
            print(numero, end=' ')
    print()


def contar(evento):
    contar = 0
    nom_hilo = threading.current_thread().getName()
    print(nom_hilo, 'en espera')
    estado = evento.wait()
    print(estado)

    while contar < 25:
        contar += 1
        print(nom_hilo, ':', contar)


evento = threading.Event()
hilo1 = threading.Thread(name='h1', target=contar, args=(evento,),)
hilo2 = threading.Thread(name='h2', target=contar, args=(evento,),)
hilo1.start()
hilo2.start()

print('Obteniendo 25 numeros pares...')
gen_pares()
print('Ya se han obtenido')
evento.set()
