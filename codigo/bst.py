class Nodo:

    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None


class BST:

    def __init__(self):
        self.raiz = None

    def buscar(self, valor, camino=None):
        """Devuelve el nodo o None y, opcionalmente, registra los nodos visitados."""
        actual = self.raiz
        while actual is not None:
            if camino is not None:
                camino.append(actual)
            if valor == actual.valor:
                return actual
            if valor < actual.valor:
                actual = actual.izquierda
            else:
                actual = actual.derecha
        return None

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

    def momentos_recorrido(self):
        """Genera (nodo, momento) antes, entre y despues de sus subarboles.

        Los tres momentos corresponden a preorder, inorder y postorder.
        No depende de coordenadas ni de objetos graficos.
        """
        def visitar(nodo):
            if nodo is None:
                return
            yield nodo, "preorder"
            yield from visitar(nodo.izquierda)
            yield nodo, "inorder"
            yield from visitar(nodo.derecha)
            yield nodo, "postorder"

        yield from visitar(self.raiz)

    def preorder(self):
        """Nodo -> Izquierda -> Derecha."""
        return [n.valor for n, momento in self.momentos_recorrido()
                if momento == "preorder"]

    def inorder(self):
        """Izquierda -> Nodo -> Derecha."""
        return [n.valor for n, momento in self.momentos_recorrido()
                if momento == "inorder"]

    def postorder(self):
        """Izquierda -> Derecha -> Nodo."""
        return [n.valor for n, momento in self.momentos_recorrido()
                if momento == "postorder"]

    def eliminar(self, valor):
        """Elimina el valor y devuelve True; devuelve False si no existe.

        Con dos hijos, copia el menor valor del subarbol derecho y retira
        ese sucesor, enlazando su posible hijo derecho con su padre.
        """
        padre = None
        actual = self.raiz
        while actual is not None and actual.valor != valor:
            padre = actual
            actual = actual.izquierda if valor < actual.valor else actual.derecha
        if actual is None:
            return False

        if actual.izquierda is not None and actual.derecha is not None:
            padre_sucesor = actual
            sucesor = actual.derecha
            while sucesor.izquierda is not None:
                padre_sucesor = sucesor
                sucesor = sucesor.izquierda
            actual.valor = sucesor.valor
            padre, actual = padre_sucesor, sucesor

        hijo = actual.izquierda if actual.izquierda is not None else actual.derecha
        if padre is None:
            self.raiz = hijo
        elif padre.izquierda is actual:
            padre.izquierda = hijo
        else:
            padre.derecha = hijo
        return True
