import threading
import time


class MyThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(),
                 kwargs=None, *, daemon=None):
        super(MyThread, self).__init__(group=group, target=target,
                                       name=name, daemon=daemon)
        self.arg1 = args[0]
        self.arg2 = args[1]

    def run(self):
        contador = 1
        while contador <= 10:
            print('ejecutando...', self.getName(), 'contador:', contador,
                  'arg1:', self.arg1,
                  'arg2:', self.arg2)
            contador += 1
            # time.sleep(0.1)


for numero in range(10):
    hilo = MyThread(args=(numero, numero*numero), daemon=False)
    hilo.start()
