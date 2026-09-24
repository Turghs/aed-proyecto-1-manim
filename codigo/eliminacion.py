"""Tres demostraciones de eliminacion sobre BST independientes del principal."""

from manim import *

from codigo.bst import BST


def estructura_visual(arbol):
    """Calcula posiciones y aristas siguiendo los enlaces actuales del BST."""
    posiciones = {}
    aristas = []

    def visitar(nodo, posicion, nivel):
        if nodo is None:
            return
        posiciones[nodo] = posicion
        for hijo, direccion in ((nodo.izquierda, LEFT), (nodo.derecha, RIGHT)):
            if hijo is not None:
                aristas.append((nodo, hijo))
                visitar(hijo, posicion + direccion * (2.4 / 2 ** nivel)
                        + DOWN * 1.7, nivel + 1)

    visitar(arbol.raiz, UP * 1.2, 0)
    return posiciones, aristas


def preparar_caso(escena, valores, eliminar, titulo, crear_nodo, crear_linea):
    arbol = BST()
    for valor in valores:
        arbol.insertar(valor)
    posiciones, aristas = estructura_visual(arbol)
    nodos = {nodo: crear_nodo(nodo.valor, posicion)
             for nodo, posicion in posiciones.items()}
    lineas = {arista: crear_linea(posiciones[arista[0]], posiciones[arista[1]])
              for arista in aristas}
    cabecera = Text(titulo, font_size=35).move_to(UP * 3.5)
    paso = Text(f"Eliminar: {eliminar}", font_size=28, color=RED).move_to(UP * 2.65)
    escena.play(FadeIn(cabecera), FadeIn(paso),
                FadeIn(VGroup(*nodos.values(), *lineas.values())), run_time=0.7)
    escena.wait(0.8)
    return arbol, nodos, lineas, cabecera, paso


def actualizar_dibujo(escena, arbol, nodos, lineas, crear_linea):
    """Anima la estructura producida por eliminar(), sin prefijar el resultado."""
    posiciones, aristas = estructura_visual(arbol)
    retirados = [nodo for nodo in nodos if nodo not in posiciones]
    desconectadas = [arista for arista in lineas if arista not in aristas]
    escena.play(*[FadeOut(nodos[nodo]) for nodo in retirados],
                *[FadeOut(lineas[arista]) for arista in desconectadas], run_time=0.65)
    for nodo in retirados:
        del nodos[nodo]
    for arista in desconectadas:
        del lineas[arista]
    cambios = [visual.animate.move_to(posiciones[nodo])
               for nodo, visual in nodos.items()]
    cambios += [Transform(linea, crear_linea(posiciones[padre], posiciones[hijo]))
                for (padre, hijo), linea in lineas.items()]
    if cambios:
        escena.play(*cambios, run_time=0.75)
    nuevas = []
    for arista in aristas:
        if arista not in lineas:
            linea = crear_linea(posiciones[arista[0]], posiciones[arista[1]])
            lineas[arista] = linea
            nuevas.append(Create(linea))
    if nuevas:
        escena.play(*nuevas, run_time=0.5)


def terminar_caso(escena, nodos, lineas, *textos):
    escena.play(FadeOut(*nodos.values(), *lineas.values(), *textos), run_time=0.5)


def caso_hoja(escena, crear_nodo, crear_linea):
    arbol, nodos, lineas, titulo, paso = preparar_caso(
        escena, (50, 30, 70), 30, "Caso 1: nodo hoja", crear_nodo, crear_linea,
    )
    elegido = arbol.buscar(30)
    escena.play(nodos[elegido][0].animate.set_stroke(RED, width=6), run_time=0.5)
    nota = Text("Sin hijos: retirar el nodo y su conexión", font_size=27)
    nota.move_to(DOWN * 3.25)
    escena.play(Write(nota), run_time=0.7)
    escena.wait(1.4)
    arbol.eliminar(elegido.valor)
    actualizar_dibujo(escena, arbol, nodos, lineas, crear_linea)
    escena.wait(1.5)
    terminar_caso(escena, nodos, lineas, titulo, paso, nota)


def caso_un_hijo(escena, crear_nodo, crear_linea):
    arbol, nodos, lineas, titulo, paso = preparar_caso(
        escena, (50, 30, 70, 40), 30, "Caso 2: un hijo", crear_nodo, crear_linea,
    )
    elegido = arbol.buscar(30)
    hijo = elegido.izquierda if elegido.izquierda is not None else elegido.derecha
    escena.play(nodos[elegido][0].animate.set_stroke(RED, width=6),
                nodos[hijo][0].animate.set_stroke(GREEN, width=6), run_time=0.6)
    nota = Text("El hijo ocupa su lugar", font_size=28, color=GREEN)
    nota.move_to(DOWN * 3.25)
    escena.play(Write(nota), run_time=0.7)
    escena.wait(1.2)
    arbol.eliminar(elegido.valor)
    actualizar_dibujo(escena, arbol, nodos, lineas, crear_linea)
    escena.wait(1.8)
    terminar_caso(escena, nodos, lineas, titulo, paso, nota)


def cambiar_paso(escena, paso, mensaje):
    nuevo = Text(mensaje, font_size=28).move_to(UP * 2.65)
    escena.play(Transform(paso, nuevo), run_time=0.6)


def caso_dos_hijos(escena, crear_nodo, crear_linea):
    arbol, nodos, lineas, titulo, paso = preparar_caso(
        escena, (50, 30, 70, 60, 80), 50, "Caso 3: dos hijos", crear_nodo, crear_linea,
    )
    elegido = arbol.buscar(50)
    escena.play(nodos[elegido][0].animate.set_stroke(RED, width=6), run_time=0.5)
    escena.wait(0.5)
    cambiar_paso(escena, paso, "1. Buscar sucesor inorder")
    nota = Text("Menor valor del subárbol derecho", font_size=27, color=YELLOW)
    nota.move_to(DOWN * 3.25)
    escena.play(Write(nota), run_time=0.7)
    anterior, sucesor = elegido, elegido.derecha
    while sucesor is not None:
        linea = lineas[(anterior, sucesor)]
        escena.play(linea.animate.set_color(YELLOW), run_time=0.35)
        marcador = Dot(linea.get_start(), radius=0.08, color=YELLOW)
        escena.add(marcador)
        escena.play(MoveAlongPath(marcador, linea), run_time=0.65)
        escena.play(FadeOut(marcador),
                    nodos[sucesor][0].animate.set_stroke(YELLOW, width=5), run_time=0.35)
        escena.wait(0.4)
        if sucesor.izquierda is None:
            break
        anterior, sucesor = sucesor, sucesor.izquierda
    escena.wait(1.1)
    cambiar_paso(escena, paso, "2. Reemplazar el valor")
    # La operacion real actualiza el valor de elegido y retira el sucesor.
    # La representacion muestra esas dos consecuencias en pasos separados.
    arbol.eliminar(elegido.valor)
    etiqueta = Text(str(elegido.valor), font_size=30).move_to(nodos[elegido].get_center())
    vieja = nodos[elegido][1]
    escena.play(FadeOut(vieja), TransformFromCopy(nodos[sucesor][1], etiqueta),
                nodos[elegido][0].animate.set_stroke(GREEN, width=6), run_time=1)
    nodos[elegido].remove(vieja)
    nodos[elegido].add(etiqueta)
    escena.wait(1.2)
    cambiar_paso(escena, paso, "3. Eliminar el sucesor original")
    escena.play(FadeOut(nota), run_time=0.3)
    actualizar_dibujo(escena, arbol, nodos, lineas, crear_linea)
    escena.wait(2)
    terminar_caso(escena, nodos, lineas, titulo, paso)


def mostrar_eliminacion(escena, crear_nodo, crear_linea):
    """Usa las funciones graficas existentes y BST locales a cada caso."""
    titulo = Text("Eliminar en un BST", font_size=36).move_to(UP)
    subtitulo = Text("Existen 3 casos", font_size=30).move_to(DOWN * 0.2)
    escena.play(Write(titulo), FadeIn(subtitulo), run_time=1)
    escena.wait(1.2)
    escena.play(FadeOut(titulo), FadeOut(subtitulo), run_time=0.4)
    caso_hoja(escena, crear_nodo, crear_linea)
    caso_un_hijo(escena, crear_nodo, crear_linea)
    caso_dos_hijos(escena, crear_nodo, crear_linea)
    titulo = Text("Eliminar en BST", font_size=36).move_to(UP * 2.5)
    resumen = VGroup(*[
        Text(texto, font_size=30, color=color)
        for texto, color in (
            ("0 hijos → eliminar", RED),
            ("1 hijo → promover hijo", GREEN),
            ("2 hijos → usar sucesor inorder", YELLOW),
        )
    ]).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(ORIGIN)
    escena.play(FadeIn(titulo), FadeIn(resumen), run_time=0.8)
    escena.wait(3)
    escena.play(FadeOut(titulo), FadeOut(resumen), run_time=0.5)
