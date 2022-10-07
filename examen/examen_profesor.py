import threading
import time

PERSONAS = 8
COMER_CONTA = 2


class Persona(threading.Thread):
    palillos = []
    conta = 0

    def __init__(self):
        super(Persona, self).__init__()
        self.id = Persona.conta
        Persona.conta += 1
        Persona.palillos.append(threading.Lock())

    def derecha(self):
        # print(str(self.id))
        return (self.id + 1) % PERSONAS

    def palillo(self):
        if self.id < self.derecha():
            Persona.palillos[self.id].acquire()
            Persona.palillos[self.derecha()].acquire()
        else:
            Persona.palillos[self.derecha()].acquire()
            Persona.palillos[self.id].acquire()

    def comer(self):
        print("Comiendo => " + str(self.id))
        time.sleep(0.10)
        print("Termino de comer => " + str(self.id))

    def libera(self):
        Persona.palillos[self.id].release()
        Persona.palillos[self.derecha()].release()

    def run(self):
        for i in range(COMER_CONTA):
            time.sleep(0.15)
            self.palillo()
            self.comer()
            self.libera()


def main():
    personas = []

    for i in range(PERSONAS):
        personas.append(Persona())

    for p in personas:
        p.start()


if __name__ == '__main__':
    main()
