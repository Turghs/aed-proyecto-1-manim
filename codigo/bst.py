class Nodo:

    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None


class BST:

    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        nuevo_nodo = Nodo(valor)

        if self.raiz is None:
            self.raiz = nuevo_nodo
            return nuevo_nodo

        actual = self.raiz
        while True:
            if valor < actual.valor:
                if actual.izquierda is None:
                    actual.izquierda = nuevo_nodo
                    return nuevo_nodo
                actual = actual.izquierda
            elif valor > actual.valor:
                if actual.derecha is None:
                    actual.derecha = nuevo_nodo
                    return nuevo_nodo
                actual = actual.derecha
            else:
                return actual
