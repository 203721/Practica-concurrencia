import threading
import time
import random

producer = random.randint(1, 10)
consumer = random.randint(1, 10)
limit = 50
storage = []


class Locker():
    def __init__(self):
        self.lock = threading.Condition()

    def ready(self):
        return self.lock.notify()

    def stop(self):
        return self.lock.wait()

    def acquire(self):
        return self.lock.acquire()

    def release(self):
        return self.lock.release()


class Producer(threading.Thread):
    count = 1

    def __init__(self, locker):
        super(Producer, self).__init__()
        self.locker = locker
        self.id = Producer.count
        Producer.count += 1

    def run(self):
        value = 0
        while True:
            if self.locker.acquire():
                if len(storage) < limit:
                    product = random.randint(1, 50)
                    storage.append(product)
                    print(
                        f"el PRODUCTOR {self.id} produjo el PRODUCTO {product}")
                    self.locker.ready()
                    self.locker.release()
                    value = self.id
                    time.sleep(2)
                else:
                    if value != self.id:
                        print(
                            f"el PRODUCTOR {self.id} quería producir pero el ALMACÉN estaba lleno")
                    self.locker.stop()


class Consumer(threading.Thread):
    count = 1

    def __init__(self, locker):
        super(Consumer, self).__init__()
        self.locker = locker
        self.id = Consumer.count
        Consumer.count += 1

    def run(self):
        value = 0
        while True:
            if self.locker.acquire():
                if storage:
                    p = random.randint(0, len(storage)-1)
                    product = storage.pop(p)
                    print(
                        f"el CONSUMIDOR {self.id} consumió el PRODUCTO {product}")
                    self.locker.ready()
                    self.locker.release()
                    value = self.id
                    time.sleep(2)
                else:
                    if value != self.id:
                        print(
                            f"el CONSUMIDOR {self.id} quería consumir pero el ALMACÉN estaba vacío")
                    self.locker.stop()


def main():
    producers = []
    consumers = []
    locker = Locker()

    print(
        f"\nHay {producer} PRODUCTORES, {consumer} CONSUMIDORES y un ALMACÉN de {limit}\n")

    for i in range(producer):
        producers.append(Producer(locker))
    for i in range(consumer):
        consumers.append(Consumer(locker))

    for p in producers:
        p.start()
    for c in consumers:
        c.start()


if __name__ == '__main__':
    main()
