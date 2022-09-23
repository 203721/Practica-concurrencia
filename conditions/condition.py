import threading

cond = threading.Condition()

# wait (s) Decrementa el valor de s si éste es mayor que
# cero. Si s es igual a 0, el proceso se bloqueará en el semáforo


class Client(threading.Thread):
    def _init_(self):
        threading.Thread._init__(self)

    def run(self):
        while True:
            cond.acquire()
            cond.wait()
            data.pop()
            cond.notify()
            cond.release()


class Server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            cond.acquire()
            if len(data) != 0:
                cond.wait()
            data.append("data 1")
            cond.notify()
            cond.release()


data = []
client = Client()
server = Server()

client.start()
server.start()

while True:
    print(data)
