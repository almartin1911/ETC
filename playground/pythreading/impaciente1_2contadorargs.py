from threading import Thread


def contar(num_hilo, **kw):
    contador = kw['inicio']
    incremento = kw['incremento']
    limite = kw['limite']

    while contador <= limite:
        print(f'Hilo: {num_hilo}, contador: {contador}')
        contador += incremento


for n_hilo in range(3):
    hilo = Thread(target=contar,
                  args=(n_hilo,),
                  kwargs={'inicio': 0, 'incremento': 1, 'limite': 10})
    hilo.start()
