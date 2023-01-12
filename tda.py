class _Nodo:
    def __init__(self, dato, prox=None):
        self.dato = dato
        self.prox = prox
    
    def __str__(self):
        return str(self.dato)

class ListaEnlazada:
    def __init__(self):
        self.prim = None
        self.len = 0
    
    def __len__(self):
        return self.len

    def __str__(self):


        res = "-->"

        actual = self.prim
        while actual:
            res += f"{actual.dato} -->"

        return res

    def append(self, dato):
        nuevo = _Nodo(dato)

        if not self.prim:
            self.prim = nuevo
        else:
            anterior = None
            actual = self.prim
            while actual:
                anterior = actual
                actual = actual.prox
            anterior.prox = nuevo

    def pop(self, i=None):
        """Elimina el nodo de la posición i, y devuelve el dato contenido.
        Si i está fuera de rango, se levanta la excepción IndexError.
        Si no se recibe la posición, devuelve el último elemento."""

        if i is None:
            i = self.len - 1

        if i < 0 or i >= self.len:
            raise IndexError("Índice fuera de rango")

        if i == 0:
        # Caso particular: saltear la cabecera de la lista
            dato = self.prim.dato
            self.prim = self.prim.prox
        else:
        # Buscar los nodos en las posiciones (i-1) e (i)
            n_ant = self.prim
            n_act = n_ant.prox
            for pos in range(1, i):
                n_ant = n_act
                n_act = n_ant.prox

            # Guardar el dato y descartar el nodo
            dato = n_act.dato
            n_ant.prox = n_act.prox

        self.len -= 1
        return dato
    
    def remove(self, x):
        """Borra la primera aparición del valor x en la lista.
        Si x no está en la lista, levanta ValueError"""

        if self.len == 0:
            raise ValueError("Lista vacía")

        if self.prim.dato == x:
            # Caso particular: saltear la cabecera de la lista
            self.prim = self.prim.prox
        else:
            # Buscar el nodo anterior al que contiene a x (n_ant)
            n_ant = self.prim
            n_act = n_ant.prox
            while n_act is not None and n_act.dato != x:
                n_ant = n_act
                n_act = n_ant.prox

            if n_act == None:
                raise ValueError("El valor no está en la lista.")

            # Descartar el nodo
            n_ant.prox = n_act.prox

        self.len -= 1

    def insert(self, i, x):
        """Inserta el elemento x en la posición i.
        Si la posición es inválida, levanta IndexError"""

        if i < 0 or i > self.len:
            raise IndexError("Posición inválida")

        nuevo = _Nodo(x)

        if i == 0:
            # Caso particular: insertar al principio
            nuevo.prox = self.prim
            self.prim = nuevo
        else:
            # Buscar el nodo anterior a la posición deseada
            n_ant = self.prim
            for pos in range(1, i):
                n_ant = n_ant.prox

            # Intercalar el nuevo nodo
            nuevo.prox = n_ant.prox
            n_ant.prox = nuevo

        self.len += 1

    # Implementar el método downsample(k) para una implementación de ListaEnlazada con referencia únicamente al primer nodo. Este método debe eliminar todo elemento de la lista que ocupe una posición que no sea múltiplo del número k pasado por parámetro (k > 1).

    # Ejemplos:
    #   L: [0, 1, 2, 3, 4, 5]                  → L.downsample(2) → L: [0, 2, 4]
    #   L: ['a', 'b', 'c', 'd', 'e', 'f', 'g'] → L.downsample(4) → L: ['a', 'e']

    def downsample(self, k):
        if not self.prim:
            return

        i = 1
        anterio = self.prim
        actual = self.prim.prox
        
        while actual:
            if i % k != 0:
                anterio.prox = actual.prox
            else:
                anterio = actual
            actual = actual.prox
            i += 1

    # Implementar un método para una implementación de ListaEnlazada con referencia únicamente al primer nodo que reciba una secuencia de números ordenados y sin repeticiones (por ejemplo, la tupla (0, 2, 6, 8)), y elimine los elementos de la lista enlazada en dichas posiciones, recorriendo la lista enlazada una única vez. Si la secuencia de índices a eliminar contiene una posición no válida se deberá lanzar una excepción. Ejemplos:

    # L: [ a b c d e ]  →  L.eliminar_posiciones([1, 3])  →  L: [ a c e ]
    # L: [ a c e ]      →  L.eliminar_posiciones([0, 2])  →  L: [ c ]
    # L: [ a c e ]      →  L.eliminar_posiciones([0, 3])  →  IndexError

    def eliminar_posiciones(self, indices):
        if not self.prim:
            raise IndexError("La lista esta vacia.")
        
        j = 0
        i = 0

        if indices[j] == 0:
            self.prim = self.prim.prox
            j += 1
            i += 1
        
        i += 1
        anterior = self.prim
        actual = self.prim.prox
        while actual:
            if i == indices[j]:
                anterior.prox = actual.prox
                actual = actual.prox
                j += 1
            else:
                anterior = actual
                actual = actual.prox
            i += 1

        if not j == len(indices):
            raise IndexError("Indices fuera de rango.")


class Pila:
    def __init__(self):
        self.items = []

    def esta_vacia(self):
        return len(self.items) == 0

    def apilar(self, item):
        self.items.append(item)
    
    def desapilar(self):
        if self.esta_vacia():
            raise IndexError("La pila esta vacia.")
        return self.items.pop()

    def ver_Tope(self):
        if self.esta_vacia():
            raise IndexError("La pila esta vacia.")
        return self.items[-1]

    def __str__(self):
        res = "--> "

        for item in self.items:
            res += str(item) + "--> "

        return res + "| Tope"

class Cola:
    def __init__(self):
        self.prim = None
        self.ult = None

    def encolar(self, item):
        nuevo = _Nodo(item)
        
        if self.ult is not None:
            self.ult.prox = nuevo
            self.ult = nuevo
        else:
            self.prim = self.ult = nuevo
    
    def desencolar(self):
        if self.prim is None:
            raise ValueError("La cola esta vacia.")

        dato = self.prim.dato
        self.prim = self.prim.prox

        if not self.prim:
            self.ult = None
        
        return dato

    def esta_vacia(self):
        return self.prim is None

    def __str__(self):
        res = "<-- "

        actual = self.prim
        while actual:
            res += str(actual.dato) + "<-- "
            actual = actual.prox

        return res