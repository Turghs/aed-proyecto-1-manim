"""Pruebas de la estructura de datos; no requieren Manim ni un render."""

import random
import unittest

from codigo.bst import BST


def construir(valores):
    arbol = BST()
    for valor in valores:
        arbol.insertar(valor)
    return arbol


class TestBST(unittest.TestCase):
    def comprobar_estructura(self, arbol, esperados):
        """Verifica enlaces, ausencia de ciclos y orden en todo el subárbol."""
        pendientes = [(arbol.raiz, float('-inf'), float('inf'))]
        vistos = set()
        valores = []
        while pendientes:
            nodo, minimo, maximo = pendientes.pop()
            if nodo is None:
                continue
            self.assertNotIn(id(nodo), vistos, 'Ciclo o nodo con varios padres')
            vistos.add(id(nodo))
            self.assertLess(minimo, nodo.valor)
            self.assertLess(nodo.valor, maximo)
            valores.append(nodo.valor)
            pendientes.append((nodo.izquierda, minimo, nodo.valor))
            pendientes.append((nodo.derecha, nodo.valor, maximo))
        self.assertEqual(sorted(valores), sorted(esperados))
        self.assertEqual(arbol.inorder(), sorted(esperados))

    def test_arbol_vacio(self):
        arbol = BST()
        camino = []
        self.assertIsNone(arbol.raiz)
        self.assertIsNone(arbol.buscar(50, camino))
        self.assertEqual(camino, [])
        self.assertFalse(arbol.eliminar(50))
        for recorrido in (arbol.preorder, arbol.inorder, arbol.postorder):
            self.assertEqual(recorrido(), [])
        self.assertEqual(list(arbol.momentos_recorrido()), [])

    def test_recorridos_del_ejemplo(self):
        arbol = construir([50, 30, 70, 20, 40, 60, 80])
        self.assertEqual(arbol.preorder(), [50, 30, 20, 40, 70, 60, 80])
        self.assertEqual(arbol.inorder(), [20, 30, 40, 50, 60, 70, 80])
        self.assertEqual(arbol.postorder(), [20, 40, 30, 60, 80, 70, 50])

    def test_momentos_de_recorrido(self):
        arbol = construir([2, 1, 3])
        eventos = [(n.valor, momento) for n, momento in arbol.momentos_recorrido()]
        self.assertEqual(eventos, [
            (2, 'preorder'),
            (1, 'preorder'), (1, 'inorder'), (1, 'postorder'),
            (2, 'inorder'),
            (3, 'preorder'), (3, 'inorder'), (3, 'postorder'),
            (2, 'postorder'),
        ])

    def test_busqueda_y_camino(self):
        arbol = construir([50, 30, 70, 20, 40, 60, 80])
        for valor, esperado, existe in [
            (50, [50], True), (60, [50, 70, 60], True),
            (65, [50, 70, 60], False), (10, [50, 30, 20], False),
        ]:
            with self.subTest(valor=valor):
                camino = []
                nodo = arbol.buscar(valor, camino)
                self.assertEqual([n.valor for n in camino], esperado)
                if existe:
                    self.assertIs(nodo, camino[-1])
                    self.assertEqual(nodo.valor, valor)
                else:
                    self.assertIsNone(nodo)

    def test_busqueda_conserva_el_camino_previo(self):
        arbol = construir([2, 1, 3])
        previo = arbol.buscar(1)
        camino = [previo]
        arbol.buscar(3, camino)
        self.assertIs(camino[0], previo)
        self.assertEqual([n.valor for n in camino], [1, 2, 3])

    def test_duplicados_devuelven_el_nodo_existente(self):
        arbol = construir([2, 1, 3])
        for valor in [2, 1, 3]:
            with self.subTest(valor=valor):
                self.assertIs(arbol.insertar(valor), arbol.buscar(valor))
                self.comprobar_estructura(arbol, [1, 2, 3])

    def test_eliminacion_casos_limite(self):
        casos = [
            ('raiz unica', [50], 50),
            ('hoja izquierda', [50, 30, 70], 30),
            ('hoja derecha', [50, 30, 70], 70),
            ('raiz con hijo izquierdo', [50, 30], 50),
            ('raiz con hijo derecho', [50, 70], 50),
            ('nodo con hijo izquierdo', [50, 30, 70, 20], 30),
            ('nodo con hijo derecho', [50, 30, 70, 80], 70),
            ('sucesor inmediato con hijo', [50, 30, 70, 80], 50),
            ('sucesor profundo hoja', [50, 30, 70, 60, 80], 50),
            ('sucesor profundo con hijo', [50, 30, 80, 60, 70], 50),
            ('dos hijos fuera de raiz', [50, 30, 70, 20, 40, 35, 37], 30),
        ]
        for nombre, valores, objetivo in casos:
            with self.subTest(caso=nombre):
                arbol = construir(valores)
                self.assertTrue(arbol.eliminar(objetivo))
                self.assertIsNone(arbol.buscar(objetivo))
                self.comprobar_estructura(arbol, set(valores) - {objetivo})
                self.assertFalse(arbol.eliminar(objetivo))

    def test_eliminar_inexistente_no_modifica_el_arbol(self):
        arbol = construir([50, 30, 70])
        raiz = arbol.raiz
        izquierda, derecha = raiz.izquierda, raiz.derecha
        self.assertFalse(arbol.eliminar(99))
        self.assertIs(arbol.raiz, raiz)
        self.assertIs(raiz.izquierda, izquierda)
        self.assertIs(raiz.derecha, derecha)
        self.comprobar_estructura(arbol, [50, 30, 70])

    def test_eliminar_todos_los_valores(self):
        for valores in (list(range(30)), list(range(29, -1, -1))):
            with self.subTest(orden=valores):
                arbol = construir(valores)
                restantes = set(valores)
                for valor in valores:
                    self.assertTrue(arbol.eliminar(valor))
                    restantes.remove(valor)
                    self.comprobar_estructura(arbol, restantes)
                self.assertIsNone(arbol.raiz)

    def test_operaciones_mezcladas_con_referencia_independiente(self):
        generador = random.Random(2026)
        for serie in range(20):
            arbol = BST()
            esperados = set()
            for paso in range(200):
                valor = generador.randrange(50)
                accion = generador.randrange(3)
                with self.subTest(serie=serie, paso=paso, valor=valor, accion=accion):
                    if accion == 0:
                        self.assertEqual(arbol.insertar(valor).valor, valor)
                        esperados.add(valor)
                    elif accion == 1:
                        self.assertEqual(arbol.eliminar(valor), valor in esperados)
                        esperados.discard(valor)
                    else:
                        nodo = arbol.buscar(valor)
                        self.assertEqual(nodo is not None, valor in esperados)
                        if nodo is not None:
                            self.assertEqual(nodo.valor, valor)
                    self.comprobar_estructura(arbol, esperados)


if __name__ == '__main__':
    unittest.main()
