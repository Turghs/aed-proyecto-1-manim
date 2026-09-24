from manim import *


from codigo.bst import BST


def crear_nodo_visual(valor, posicion):
    circulo = Circle(radius=0.55, color=BLUE, fill_color=BLUE_E, fill_opacity=1)
    circulo.move_to(posicion)
    etiqueta = Text(str(valor), font_size=30).move_to(circulo.get_center())
    return VGroup(circulo, etiqueta)


def mostrar_comparacion(self, expresion):
    comparacion = Text(expresion, font_size=32).to_edge(UP)
    self.play(Write(comparacion))
    self.wait(1)
    self.play(FadeOut(comparacion))


def mostrar_algoritmo(self):
    arbol = BST()

    posicion_raiz = UP * 1.5
    posicion_izquierda = LEFT * 2 + DOWN * 0.5
    posicion_derecha = RIGHT * 2 + DOWN * 0.5

    nodo_50 = crear_nodo_visual(arbol.insertar(50).valor, posicion_raiz)
    self.play(Create(nodo_50[0]), Write(nodo_50[1]))
    self.wait(1)

    mostrar_comparacion(self, "30 < 50")
    nodo_30 = crear_nodo_visual(arbol.insertar(30).valor, posicion_izquierda)
    conexion_izquierda = Line(
        nodo_50[0].get_bottom(),
        nodo_30[0].get_top(),
        color=WHITE,
    )
    self.play(Create(conexion_izquierda), Create(nodo_30[0]), Write(nodo_30[1]))
    self.wait(1)

    mostrar_comparacion(self, "70 > 50")
    nodo_70 = crear_nodo_visual(arbol.insertar(70).valor, posicion_derecha)
    conexion_derecha = Line(
        nodo_50[0].get_bottom(),
        nodo_70[0].get_top(),
        color=WHITE,
    )
    self.play(Create(conexion_derecha), Create(nodo_70[0]), Write(nodo_70[1]))

    self.wait(3)
    self.play(
        FadeOut(
            nodo_50,
            nodo_30,
            nodo_70,
            conexion_izquierda,
            conexion_derecha,
        )
    )
