"""Animaciones de recorridos sobre el BST y los nodos visuales existentes."""

from manim import *


ORDENES = ("preorder", "inorder", "postorder")
COLORES = {"preorder": ORANGE, "inorder": GREEN, "postorder": PURPLE_A}
REGLAS = {
    "preorder": "Nodo → Izquierda → Derecha",
    "inorder": "Izquierda → Nodo → Derecha",
    "postorder": "Izquierda → Derecha → Nodo",
}
DESPLAZAMIENTOS = {"preorder": LEFT, "inorder": DOWN, "postorder": RIGHT}


def crear_puntos(nodos):
    # Radio del nodo escalado: 0.44. Los puntos quedan fuera, con margen.
    return {
        (nodo, orden): Dot(
            visual.get_center() + DESPLAZAMIENTOS[orden] * 0.61,
            radius=0.065, color=COLORES[orden],
        ).set_z_index(2)
        for nodo, visual in nodos.items()
        for orden in ORDENES
    }


def crear_leyenda():
    posiciones = ("Izquierdo", "Inferior", "Derecho")
    entradas = [
        VGroup(
            Dot(radius=0.055, color=COLORES[orden]),
            Text(f"{posicion} → {orden.capitalize()}", font_size=19),
        ).arrange(RIGHT, buff=0.12)
        for orden, posicion in zip(ORDENES, posiciones)
    ]
    return VGroup(*entradas).arrange(RIGHT, buff=0.5).move_to(UP * 2.35)


def mover_indicador(escena, indicador, anterior, evento, puntos, duracion):
    destino = puntos[evento].get_center()
    if anterior is not None and anterior[0] is evento[0]:
        # En una hoja se ve el paso izquierdo -> inferior -> derecho.
        trayectoria = ArcBetweenPoints(
            indicador.get_center(), destino, angle=PI / 2,
        )
    else:
        trayectoria = Line(indicador.get_center(), destino)
    escena.play(MoveAlongPath(indicador, trayectoria), run_time=duracion,
                rate_func=linear)


def crear_secuencia(valores, color):
    # Los espacios quedan reservados, pero cada elemento se revela al visitarlo.
    elementos = []
    for indice, valor in enumerate(valores):
        if indice:
            elementos.append(Text("→", font_size=28, color=color))
        elementos.append(Text(str(valor), font_size=28, color=color))
    grupo = VGroup(*elementos).arrange(RIGHT, buff=0.17)
    if grupo.width > 12:
        grupo.scale_to_fit_width(12)
    return grupo.move_to(DOWN * 2.85)


def explicar_contorno(escena, eventos, puntos):
    texto = Text("Sigamos el contorno: cada nodo tiene tres momentos", font_size=25)
    texto.move_to(UP * 2.95)
    nota = Text("El punto que elegimos determina el orden de visita", font_size=25)
    nota.move_to(DOWN * 2.85)
    escena.play(Write(texto), FadeIn(nota))
    escena.wait(1.5)
    indicador = Circle(radius=0.105, color=WHITE, stroke_width=2).set_z_index(3)
    indicador.move_to(puntos[eventos[0]].get_center())
    escena.play(FadeIn(indicador), run_time=0.3)
    anterior = None
    for evento in eventos:
        if anterior is not None:
            mover_indicador(escena, indicador, anterior, evento, puntos, 0.3)
        escena.play(Indicate(puntos[evento], color=COLORES[evento[1]],
                            scale_factor=1.4), run_time=0.2)
        anterior = evento
    escena.wait(1)
    escena.play(FadeOut(indicador), FadeOut(texto), FadeOut(nota))


def animar_recorrido(escena, orden, valores, eventos, nodos, puntos):
    color = COLORES[orden]
    titulo = Text(orden.upper(), font_size=34, color=color).move_to(UP * 3.55)
    regla = Text(REGLAS[orden], font_size=26).move_to(UP * 2.95)
    escena.play(
        FadeIn(titulo), FadeIn(regla),
        *[punto.animate.set_opacity(1 if momento == orden else 0.25)
          for (_, momento), punto in puntos.items()],
    )
    escena.wait(1)
    secuencia = crear_secuencia(valores, color)
    indicador = Circle(radius=0.105, color=WHITE, stroke_width=2).set_z_index(3)
    indicador.move_to(puntos[eventos[0]].get_center())
    escena.play(FadeIn(indicador), run_time=0.3)
    anterior = None
    ultimo_visual = None
    visitados = 0
    for evento in eventos:
        if anterior is not None:
            mover_indicador(escena, indicador, anterior, evento, puntos, 0.28)
        nodo, momento = evento
        if momento == orden:
            visual = nodos[nodo]
            cambios = [visual[0].animate.set_stroke(color, width=5)]
            if ultimo_visual is not None:
                cambios.append(ultimo_visual[0].animate.set_stroke(BLUE, width=4))
            # Cada evento proviene de la misma logica que genero el resultado.
            assert nodo.valor == valores[visitados]
            nuevos = [secuencia[0]] if visitados == 0 else [
                secuencia[2 * visitados - 1], secuencia[2 * visitados]
            ]
            escena.play(
                *cambios, *[FadeIn(elemento, shift=UP * 0.1) for elemento in nuevos],
                Indicate(puntos[evento], color=color, scale_factor=1.5),
                run_time=0.55,
            )
            escena.wait(0.4)
            ultimo_visual = visual
            visitados += 1
        anterior = evento
    escena.play(FadeOut(indicador), run_time=0.3)
    nota = None
    if orden == "inorder":
        nota = Text(
            "En un BST, Inorder produce los valores en orden ascendente",
            font_size=22, color=color,
        ).move_to(DOWN * 3.5)
        escena.play(Write(nota))
        escena.wait(3)
    else:
        escena.wait(2)
    salida = [titulo, regla, secuencia]
    if nota is not None:
        salida.append(nota)
    cambios = [FadeOut(*salida)]
    if ultimo_visual is not None:
        cambios.append(ultimo_visual[0].animate.set_stroke(BLUE, width=4))
    escena.play(*cambios)


def mostrar_recorridos(escena, arbol, nodos, conexiones):
    titulo = Text("Recorridos de un BST", font_size=36).move_to(UP * 3.55)
    escena.play(Write(titulo))
    escena.wait(1)
    # Reutiliza exactamente los objetos del arbol construido. Solo esta seccion
    # usa una escala menor para reservar espacio a leyenda, puntos y resultados.
    for visual in nodos.values():
        visual[0].set_stroke(BLUE, width=4)
    for linea in conexiones.values():
        linea.set_color(WHITE)
    dibujo = VGroup(*nodos.values(), *conexiones.values())
    dibujo.scale(0.8, about_point=ORIGIN).shift(UP * 0.15)
    puntos = crear_puntos(nodos)
    grupo_puntos = VGroup(*puntos.values())
    leyenda = crear_leyenda()
    escena.play(FadeIn(dibujo), FadeIn(grupo_puntos), FadeIn(leyenda))
    eventos = list(arbol.momentos_recorrido())
    resultados = {orden: getattr(arbol, orden)() for orden in ORDENES}
    explicar_contorno(escena, eventos, puntos)
    escena.play(FadeOut(titulo), run_time=0.5)
    for orden in ORDENES:
        animar_recorrido(escena, orden, resultados[orden], eventos, nodos, puntos)
    escena.play(FadeOut(dibujo), FadeOut(grupo_puntos), FadeOut(leyenda))
    resumen_titulo = Text("Tres recorridos, un mismo BST", font_size=36).to_edge(UP)
    filas = VGroup(*[
        Text(
            f"{orden.upper()}:  " + " → ".join(map(str, resultados[orden])),
            font_size=29, color=COLORES[orden],
        )
        for orden in ORDENES
    ]).arrange(DOWN, aligned_edge=LEFT, buff=0.65)
    if filas.width > 12.5:
        filas.scale_to_fit_width(12.5)
    filas.move_to(ORIGIN)
    escena.play(Write(resumen_titulo), FadeIn(filas))
    escena.wait(5)
    escena.play(FadeOut(resumen_titulo), FadeOut(filas))
