import threading
import time

mutex = threading.Lock()


def acciones(persona):
    print(f"\nPersonas que esperan: {esperando}")
    time.sleep(2)
    persona.izquierda.tomar(persona.id, "izquierda")
    persona.derecha.tomar(persona.id, "derecha")
    time.sleep(2)
    print(f"Persona {persona.id} come...")
    time.sleep(2)
    persona.derecha.dejar(persona.id, "derecha")
    persona.izquierda.dejar(persona.id, "izquierda")
    time.sleep(2)
    esperando.remove(persona.id)
    if not esperando:
        print(
            f"\nPersonas que esperan: {esperando}\nTodas las personas han comido una vez.")


class Palillo(object):
    def __init__(self, numero):
        self.numero = numero+1
        self.tomado = False

    def tomar(self, usuario, direccion):
        if self.tomado == False:
            self.tomado = True
            print(
                f"Persona {usuario} toma el palillo {self.numero}, que está a su {direccion}.")

    def dejar(self, usuario, direccion):
        self.tomado = False
        print(
            f"Persona {usuario} deja el palillo {self.numero} en su {direccion}.")


class Persona(threading.Thread):
    def __init__(self, id, izquierda, derecha):
        threading.Thread.__init__(self)
        self.id = id+1
        self.izquierda = izquierda
        self.derecha = derecha

    def run(self):
        mutex.acquire()
        acciones(self)
        mutex.release()


if __name__ == "__main__":
    n = 8
    palillos = []
    personas = []
    esperando = []
    for i in range(n):
        palillos.append(Palillo(i))
    for i in range(n):
        personas.append(Persona(i, palillos[i], palillos[(i+1) % n]))
    for i in personas:
        esperando.append(i.id)
    for i in range(n):
        personas[i].start()
