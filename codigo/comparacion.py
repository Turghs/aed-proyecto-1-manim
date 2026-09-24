"""Forma, altura y costo de buscar en dos BST construidos por insercion."""

from manim import *

from codigo.bst import BST


BALANCEADO = (50, 30, 70, 20, 40, 60, 80)
DEGENERADO = (20, 30, 40, 50, 60, 70, 80)
ESCALA = 0.6


def crear_ejemplo(valores, origen, paso_x, paso_y, reducir, crear_nodo, crear_linea):
    arbol = BST()
    for valor in valores:
        arbol.insertar(valor)
    nodos, lineas = {}, {}

    def dibujar(nodo, posicion, nivel=0):
        nodos[nodo] = crear_nodo(nodo.valor, posicion).scale(ESCALA)
        distancia = paso_x / 2 ** nivel if reducir else paso_x
        for hijo, direccion in ((nodo.izquierda, LEFT), (nodo.derecha, RIGHT)):
            if hijo is not None:
                destino = posicion + direccion * distancia + DOWN * paso_y
                # Escala tambien el margen de la funcion de conexiones original.
                lineas[(nodo, hijo)] = crear_linea(
                    posicion / ESCALA, destino / ESCALA,
                ).scale(ESCALA, about_point=ORIGIN)
                dibujar(hijo, destino, nivel + 1)

    dibujar(arbol.raiz, origen)
    return arbol, nodos, lineas


def animar_costo_busqueda(escena, ejemplo, contador, color):
    arbol, nodos, lineas = ejemplo
    camino = []
    encontrado = arbol.buscar(80, camino)
    for indice, nodo in enumerate(camino):
        if indice:
            linea = lineas[(camino[indice - 1], nodo)]
            escena.play(linea.animate.set_color(color), run_time=0.18)
        cantidad = indice + 1
        etiqueta = "comparación" if cantidad == 1 else "comparaciones"
        nuevo = Text(f"{cantidad} {etiqueta}", font_size=26, color=color)
        nuevo.move_to(contador.get_center())
        escena.play(nodos[nodo][0].animate.set_stroke(color, width=5),
                    Transform(contador, nuevo), run_time=0.45)
    assert encontrado is camino[-1] and encontrado.valor == 80


def mostrar_comparacion_bst(escena, crear_nodo, crear_linea):
    titulo = Text("¿La forma del BST importa?", font_size=36).move_to(UP * 0.8)
    respuesta = Text("Sí: determina cuántos nodos debemos recorrer.", font_size=28)
    respuesta.move_to(DOWN * 0.4)
    escena.play(Write(titulo), FadeIn(respuesta), run_time=1)
    escena.wait(1.8)
    escena.play(FadeOut(titulo), FadeOut(respuesta), run_time=0.4)

    izquierdo = crear_ejemplo(
        BALANCEADO, LEFT * 3.55 + UP * 1.6, 1.55, 1.45, True,
        crear_nodo, crear_linea,
    )
    derecho = crear_ejemplo(
        DEGENERADO, RIGHT * 1.5 + UP * 1.6, 0.64, 0.56, False,
        crear_nodo, crear_linea,
    )
    dibujos = VGroup(*izquierdo[1].values(), *izquierdo[2].values(),
                     *derecho[1].values(), *derecho[2].values())
    titulo = Text("Buscar el mismo valor: 80", font_size=34).move_to(UP * 3.5)
    etiquetas = VGroup(
        Text("BST relativamente balanceado", font_size=24).move_to(LEFT * 3.55 + UP * 2.65),
        Text("BST degenerado", font_size=24).move_to(RIGHT * 3.55 + UP * 2.65),
    )
    divisor = Line(UP * 2.25, DOWN * 3.65, color=GREY, stroke_width=1)
    contadores = VGroup(*[
        Text("0 comparaciones", font_size=26, color=color).move_to(RIGHT * x + DOWN * 2.55)
        for x, color in ((-3.55, GREEN), (3.55, ORANGE))
    ])
    nota = Text("1 comparación = 1 nodo inspeccionado", font_size=20).move_to(DOWN * 3.45)
    escena.play(FadeIn(titulo), FadeIn(etiquetas), FadeIn(divisor),
                FadeIn(dibujos), FadeIn(contadores), FadeIn(nota), run_time=0.8)
    escena.wait(0.4)
    animar_costo_busqueda(escena, izquierdo, contadores[0], GREEN)
    escena.wait(0.6)
    animar_costo_busqueda(escena, derecho, contadores[1], ORANGE)
    escena.wait(1.6)

    explicacion = Text("La eficiencia depende de la altura del árbol", font_size=30)
    explicacion.move_to(UP * 3.5)
    escena.play(Transform(titulo, explicacion), FadeOut(nota), run_time=0.6)
    costos = VGroup(*[
        VGroup(Text(altura, font_size=19), Text(costo, font_size=30, color=color))
        .arrange(DOWN, buff=0.08).move_to(RIGHT * x + DOWN * 3.25)
        for x, altura, costo, color in (
            (-3.55, "Altura logarítmica", "O(log n)", GREEN),
            (3.55, "Altura lineal", "O(n)", ORANGE),
        )
    ])
    escena.play(FadeIn(costos), run_time=0.5)
    escena.wait(2.8)
    escena.play(FadeOut(titulo), FadeOut(etiquetas), FadeOut(divisor),
                FadeOut(dibujos), FadeOut(contadores), FadeOut(costos), run_time=0.5)

    titulo = Text("El orden de inserción importa", font_size=34).move_to(UP * 2)
    secuencia = Text(
        " → ".join(map(str, DEGENERADO)), font_size=28,
    ).move_to(UP * 0.8)
    flecha = Text("↓", font_size=34).move_to(ORIGIN)
    efecto = Text("Un BST común puede degenerarse", font_size=29, color=ORANGE)
    efecto.move_to(DOWN * 0.85)
    garantia = Text("No garantiza O(log n)", font_size=27).move_to(DOWN * 1.85)
    tarjeta = VGroup(titulo, secuencia, flecha, efecto, garantia)
    escena.play(FadeIn(tarjeta), run_time=1)
    escena.wait(2.8)
    escena.play(FadeOut(tarjeta), run_time=0.4)
    mensaje = Text(
        "Un BST eficiente busca mantener\nuna altura pequeña", font_size=34,
    )
    escena.play(Write(mensaje), run_time=0.8)
    escena.wait(1.8)
    escena.play(FadeOut(mensaje), run_time=0.4)
