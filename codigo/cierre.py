from manim import *


INTEGRANTES = ('Escobar Hinojosa, Darlene Priyanka', 'Luciani Dávila, Itzel Yadira Arellys', 'Vasquez de Velasco Quintana, Nicolás Agustín')


def mostrar_cierre(escena):
    titulo = Text("Binary Search Tree", font="Arial", font_size=40, weight=BOLD)
    titulo.move_to(UP * 2.9)
    temas = ("Inserción", "Búsqueda", "Recorridos", "Eliminación",
             "Eficiencia según la altura")
    filas = VGroup(*[
        VGroup(VMobject(color=GREEN, stroke_width=4).set_points_as_corners(
            [LEFT * 0.12, DOWN * 0.1, RIGHT * 0.22 + UP * 0.17]),
               Text(tema, font="Arial", font_size=25)).arrange(RIGHT, buff=0.18)
        for tema in temas
    ]).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(UP * 0.2)
    conclusion = Text(
        "La eficiencia de un BST depende de la forma y altura del árbol.",
        font="Arial", font_size=24,
    ).move_to(DOWN * 2.25)
    escena.play(FadeIn(titulo), run_time=0.6)
    escena.play(LaggedStart(*[FadeIn(fila, shift=RIGHT * 0.15) for fila in filas],
                           lag_ratio=0.25), run_time=1.5)
    escena.play(FadeIn(conclusion), run_time=0.5)
    escena.wait(2)
    escena.play(FadeOut(filas, conclusion), run_time=0.5)
    creditos = VGroup(*[
        Text(nombre, font="Arial", font_size=24) for nombre in INTEGRANTES
    ]).arrange(DOWN, buff=0.3).move_to(UP * 0.2)
    curso = Text("Algoritmos y Estructuras de Datos", font="Arial", font_size=27,
                 color=BLUE).move_to(DOWN * 2.25)
    escena.play(FadeIn(creditos), FadeIn(curso), run_time=0.7)
    escena.wait(3.5)
    escena.play(FadeOut(titulo, creditos, curso), run_time=0.7)
