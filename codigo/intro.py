from manim import *

from codigo.algoritmo import crear_nodo_visual, crear_conexion


def mostrar_intro(escena):
    titulo = Text("Binary Search Tree", font="Arial", font_size=42, weight=BOLD)
    titulo.move_to(LEFT * 2.6 + UP * 1.35)
    subtitulo = Text("Árbol Binario de Búsqueda (BST)", font="Arial", font_size=24)
    subtitulo.move_to(LEFT * 2.6 + UP * 0.35)
    acento = Line(LEFT * 5.7 + UP * 0.8, LEFT * 0.1 + UP * 0.8,
                  color=BLUE, stroke_width=4)
    posiciones = [RIGHT * 3.7 + UP * 1.4,
                  RIGHT * 2.2 + DOWN * 0.5, RIGHT * 5.2 + DOWN * 0.5]
    nodos = [crear_nodo_visual(valor, posicion).scale(0.8)
             for valor, posicion in zip((50, 30, 70), posiciones)]
    lineas = [crear_conexion(posiciones[0] / 0.8, posicion / 0.8)
              .scale(0.8, about_point=ORIGIN) for posicion in posiciones[1:]]
    frase = Text("Buscar, insertar y organizar datos eficientemente",
                 font="Arial", font_size=26).move_to(DOWN * 2.25)
    escena.play(FadeIn(titulo, shift=UP * 0.2), Create(acento), run_time=0.9)
    escena.play(FadeIn(subtitulo), GrowFromCenter(nodos[0]), run_time=0.8)
    for linea, nodo in zip(lineas, nodos[1:]):
        escena.play(Create(linea), GrowFromCenter(nodo), run_time=0.7)
    escena.play(FadeIn(frase, shift=UP * 0.15),
                Indicate(nodos[0], color=BLUE, scale_factor=1.08), run_time=0.8)
    escena.wait(3)
    escena.play(FadeOut(titulo, subtitulo, acento, frase, *nodos, *lineas), run_time=0.7)
