# Bryan Alexander Morales Roblero 203721
# Enrique de Jesús Farrera Sánchez 203467
import threading
import time
import random
from queue import Queue

# In case we want to use a random number of clients:
# clients_number = random.randint(10, 30)
clients_number = 22
capacity = 20
waiter_number = chef_number = int(capacity * 0.1)
reservation_number = int(capacity * 0.2)


class Monitor():
    mutex = threading.Lock()
    # Conditions
    capacity_condition = threading.Condition()
    waiter_condition = threading.Condition()
    chef_condition = threading.Condition()
    reservation_condition = threading.Condition()
    # Queues
    restaurant_queue = Queue(capacity)
    orders = Queue()
    food = Queue()
    reservation_queue = Queue(reservation_number)

    def __init__(self):
        super(Monitor, self).__init__()

    def _without_reservation(self, client):
        self.reservation_condition.acquire()
        print(f"CLIENTE {str(client.id)} llegó al restaurante")
        time.sleep(1)

        self.mutex.acquire()
        self._enter(client)

        self.reservation_condition.notify()
        self.reservation_condition.release()

    def _reservation(self, client):
        self.reservation_condition.acquire()
        if self.reservation_queue.full():
            self.reservation_condition.wait()
        else:
            self.reservation_queue.put(client)
            print(
                f"CLIENTE {str(client.id)} ingresó a la cola, con reservación")
            time.sleep(4)
            print(
                f"CLIENTE {str(client.id)} llegó al restaurante, con reservación")
            time.sleep(1)

            self.mutex.acquire()
            self._enter(client)
            self.reservation_queue.get()

            self.reservation_condition.notify()
            self.reservation_condition.release()

    def _enter(self, client):
        self.capacity_condition.acquire()
        if self.restaurant_queue.full():
            print(f"CLIENTE {str(client.id)} está esperando una mesa")
            self.capacity_condition.wait()
        else:
            print(f"CLIENTE {str(client.id)} entró al restaurante")
            time.sleep(2)
            self.restaurant_queue.put(client)
            print(f"RECEPCIONISTA asignó una mesa a CLIENTE {str(client.id)}")

            self.waiter_condition.acquire()
            self.waiter_condition.notify()
            self.waiter_condition.release()

            self.mutex.release()
            self.capacity_condition.release()

    def _serve(self, waiter):
        while True:
            time.sleep(2)
            self.waiter_condition.acquire()
            if self.restaurant_queue.empty():
                print(f"MESERO {str(waiter.id)} está descansando")
                self.waiter_condition.wait()
            else:
                client = self.restaurant_queue.get()
                if client.served == False:
                    print(
                        f"MESERO {str(waiter.id)} está atendiendo a CLIENTE {str(client.id)}")
                    print(
                        f"el pedido de CLIENTE {str(client.id)} se añadió a la cola")
                    self.orders.put(client.id)

                    self.chef_condition.acquire()
                    self.chef_condition.notify()
                    self.chef_condition.release()

                    client.served = True
                    self.waiter_condition.release()
                else:
                    self.waiter_condition.release()

    def _cooking(self, chef):
        while True:
            time.sleep(1)
            self.chef_condition.acquire()
            if self.orders.empty():
                print(f"COCINERO {str(chef.id)} está descansando")
                self.chef_condition.wait()
            else:
                order = self.orders.get()
                print(
                    f"COCINERO {str(chef.id)} está cocinando el pedido de CLIENTE {order}")
                time.sleep(3)
                print(f"el pedido de CLIENTE {order} está listo")
                self.food.put(order)
                self.chef_condition.release()

    def _eat(self):
        time.sleep(1)
        if not self.food.empty():
            client = self.food.get()
            print(f"CLIENTE {client} está comiendo")
            time.sleep(4)
            print(f"CLIENTE {client} terminó de comer")
            print(f"CLIENTE {client} se fué feliz del restaurante")


class Client(threading.Thread):
    count = 1
    served = False

    def __init__(self, reservation):
        super(Client, self).__init__()
        self.id = Client.count
        self.reservation = reservation
        Client.count += 1

    def run(self):
        time.sleep(0.2)
        if self.reservation:
            monitor._reservation(self)
        else:
            monitor._without_reservation(self)
        monitor._eat()


class Waiter(threading.Thread):
    count = 1

    def __init__(self):
        super(Waiter, self).__init__()
        self.id = Waiter.count
        Waiter.count += 1

    def run(self):
        monitor._serve(self)


class Chef(threading.Thread):
    count = 1

    def __init__(self):
        super(Chef, self).__init__()
        self.id = Chef.count
        Chef.count += 1

    def run(self):
        monitor._cooking(self)


def main():
    clients = []
    waiters = []
    chefs = []

    print(f"\nBienvenido al restaurante UPPRO\n")

    for i in range(clients_number):
        reservation_luck = bool(random.choice([0, 0, 1]))
        clients.append(Client(reservation_luck))
    for i in range(waiter_number):
        waiters.append(Waiter())
    for i in range(chef_number):
        chefs.append(Chef())

    for client in clients:
        client.start()
    for waiter in waiters:
        waiter.start()
    for chef in chefs:
        chef.start()


if __name__ == '__main__':
    monitor = Monitor()
    main()
