from manim import *


from codigo.bst import BST
from codigo.recorridos import mostrar_recorridos
from codigo.eliminacion import mostrar_eliminacion
from codigo.comparacion import mostrar_comparacion_bst


def crear_nodo_visual(valor, posicion):
    circulo = Circle(radius=0.55, color=BLUE, fill_color=BLUE_E, fill_opacity=1)
    circulo.move_to(posicion)
    etiqueta = Text(str(valor), font_size=30).move_to(circulo.get_center())
    return VGroup(circulo, etiqueta)


def crear_conexion(origen, destino):
    # El margen recorta la linea en el borde de ambos circulos.
    return Line(origen, destino, buff=0.55, color=WHITE).set_z_index(-1)


def mostrar_comparacion(escena, valor, actual, visual):
    izquierda = valor < actual.valor
    operador = "<" if izquierda else ">"
    direccion = "izquierda" if izquierda else "derecha"
    texto = Text(
        f"{valor} {operador} {actual.valor}  →  {direccion}", font_size=30
    ).move_to(UP * 2.65)
    escena.play(visual[0].animate.set_stroke(YELLOW, width=5), Write(texto))
    escena.wait(0.5)
    return texto, izquierda


def animar_insercion(escena, arbol, valor, nodos, conexiones):
    encabezado = Text(f"Insertando: {valor}", font_size=36).to_edge(UP)
    escena.play(FadeIn(encabezado), run_time=0.4)
    actual = arbol.raiz
    padre = None
    posicion = UP * 1.5
    profundidad = 0
    camino_nodos = []
    camino_lineas = []

    while actual is not None:
        # Se siguen los enlaces del BST, no una lista de comparaciones prefijada.
        visual = nodos[actual]
        if valor == actual.valor:
            escena.play(Indicate(visual), FadeOut(encabezado))
            return
        texto, izquierda = mostrar_comparacion(escena, valor, actual, visual)
        camino_nodos.append(visual)
        padre = actual
        siguiente = actual.izquierda if izquierda else actual.derecha
        desplazamiento = 3 / (2 ** profundidad)
        posicion = visual.get_center() + DOWN * 1.8
        posicion += (LEFT if izquierda else RIGHT) * desplazamiento

        if siguiente is None:
            linea = crear_conexion(visual.get_center(), posicion)
            conexiones[(padre, valor)] = linea
            escena.play(Create(linea.set_color(YELLOW)), run_time=0.6)
        else:
            linea = conexiones[(actual, siguiente.valor)]
            escena.play(linea.animate.set_color(YELLOW), run_time=0.4)
        camino_lineas.append(linea)

        marcador = Dot(linea.get_start(), radius=0.08, color=YELLOW)
        escena.add(marcador)
        escena.play(MoveAlongPath(marcador, linea), run_time=0.7)
        escena.play(FadeOut(marcador), FadeOut(texto), run_time=0.3)
        actual = siguiente
        profundidad += 1

    nuevo = arbol.insertar(valor)
    visual = crear_nodo_visual(nuevo.valor, posicion)
    nodos[nuevo] = visual
    escena.play(Create(visual[0]), Write(visual[1]), run_time=0.7)
    escena.play(Indicate(visual, color=GREEN), run_time=0.5)
    escena.wait(0.4)
    escena.play(
        *[nodo[0].animate.set_stroke(BLUE, width=4) for nodo in camino_nodos],
        *[linea.animate.set_color(WHITE) for linea in camino_lineas],
        FadeOut(encabezado),
        run_time=0.4,
    )


def animar_busqueda(escena, arbol, valor, nodos, conexiones):
    camino = []
    encontrado = arbol.buscar(valor, camino)
    titulo = Text("Búsqueda en un BST", font_size=36).to_edge(UP)
    escena.play(Write(titulo))
    escena.wait(1)

    for indice, actual in enumerate(camino):
        visual = nodos[actual]
        if indice:
            anterior = camino[indice - 1]
            linea = conexiones[(anterior, actual.valor)]
            escena.play(
                nodos[anterior][0].animate.set_stroke(BLUE, width=4),
                linea.animate.set_color(YELLOW),
                run_time=0.5,
            )
            marcador = Dot(linea.get_start(), radius=0.08, color=YELLOW)
            escena.add(marcador)
            escena.play(MoveAlongPath(marcador, linea), run_time=0.8)
            escena.play(FadeOut(marcador), run_time=0.2)

        if actual is encontrado:
            texto = Text(f"{valor} = {actual.valor}", font_size=30)
        else:
            izquierda = valor < actual.valor
            operador = "<" if izquierda else ">"
            direccion = "izquierda" if izquierda else "derecha"
            texto = Text(
                f"{valor} {operador} {actual.valor} → {direccion}", font_size=30
            )
        texto.move_to(UP * 2.65)
        escena.play(visual[0].animate.set_stroke(YELLOW, width=5), Write(texto))
        escena.wait(1.8)
        if actual is not encontrado:
            escena.play(FadeOut(texto), run_time=0.3)

    mensaje = "¡Elemento encontrado!" if encontrado is not None else "Elemento no encontrado"
    resultado = Text(
        mensaje, font_size=32, color=GREEN if encontrado is not None else RED
    ).move_to(DOWN * 3.3)
    if encontrado is not None:
        escena.play(
            nodos[encontrado][0].animate.set_stroke(GREEN, width=6),
            Write(resultado),
        )
    else:
        escena.play(Write(resultado))
    escena.wait(3)
    textos = [titulo, resultado]
    if encontrado is not None:
        textos.append(texto)
    escena.play(FadeOut(*textos))


def mostrar_algoritmo(self, incluir_busqueda=True):
    arbol = BST()
    nodos = {}
    conexiones = {}
    for valor in (50, 30, 70, 20, 40, 60, 80):
        animar_insercion(self, arbol, valor, nodos, conexiones)

    self.wait(4)
    if incluir_busqueda:
        animar_busqueda(self, arbol, 60, nodos, conexiones)
    # Conserva la transicion que main.py necesita hacia el cierre existente.
    self.play(FadeOut(*nodos.values(), *conexiones.values()))
    if incluir_busqueda:
        mostrar_recorridos(self, arbol, nodos, conexiones)
        mostrar_eliminacion(self, crear_nodo_visual, crear_conexion)
        mostrar_comparacion_bst(self, crear_nodo_visual, crear_conexion)


class ConstruccionBST(Scene):
    """Permite renderizar solo la construccion, sin introduccion ni cierre."""

    def construct(self):
        mostrar_algoritmo(self, incluir_busqueda=False)
