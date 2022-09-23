from threading import Thread
import threading

mutex = threading.Lock()


def crito(id):
    global x;
    x = x + id
    print("Hilo =" + str(id) + " =>" + str(x))
    x = 1


class Hilo(Thread):
    def __init__(self, id):
        Thread.__init__(self)
        self.id = id

    def run(self):
        mutex.acquire()
        crito(self.id)
        # print("valor " + str(self.id))
        mutex.release()


hilos = [Hilo(1), Hilo(2), Hilo(3)]
x = 1;
for h in hilos:
    h.start()
