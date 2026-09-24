from manim import *


def mostrar_explicacion(escena):
    titulo = Text("¿Qué es un BST?", font_size=36).move_to(UP * 2)
    definicion = Text("Cada nodo organiza sus subárboles por valor", font_size=28)
    regla = VGroup(
        Text("Izquierda: menores", font_size=28, color=BLUE),
        Text("Derecha: mayores", font_size=28, color=GREEN),
    ).arrange(RIGHT, buff=1).move_to(DOWN * 1)
    escena.play(Write(titulo), FadeIn(definicion), FadeIn(regla))
    escena.wait(3)
    escena.play(FadeOut(titulo, definicion, regla))
