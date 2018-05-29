# Based on:
# https://www.troyfawkes.com/learn-python-multithreading-queues-basics/
import queue
import threading


def do_stuff(q, event):
    event.wait()
    while not q.empty():
        print(threading.current_thread().name, q.get())
        q.task_done()


def populate_queue(q, event):
    c = 0
    while c < 20:
        c += 1
        print(threading.current_thread().name, 'contador:', c)
        q.put(c)
    event.set()


q = queue.Queue(maxsize=0)
num_threads = 10

event = threading.Event()
populate = threading.Thread(target=populate_queue, args=(q, event))
populate.start()

for i in range(num_threads):
    worker = threading.Thread(target=do_stuff, args=(q, event))
    worker.start()

# q.join()
