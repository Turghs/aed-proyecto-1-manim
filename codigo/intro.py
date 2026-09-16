from manim import *

def mostrar_intro(self):
    titulo = Text("Proyecto 1 - Animando Estructuras de Datos")
    integrantes = Text(
        "Darlene Priyanka Escobar Hinojosa\n"
        "Itzel Yadira Arellys Luciani Dávila\n"
        "Nicolás Agustín Vasquez de Velasco Quintana",
        font_size=24
    )

    integrantes.next_to(titulo, DOWN)

    self.play(Write(titulo))
    self.play(FadeIn(integrantes))
    self.wait(3)

    self.play(FadeOut(titulo), FadeOut(integrantes))