from manim import *

def mostrar_cierre(self):
    texto = Text("Fin")

    self.play(Write(texto))
    self.wait(2)