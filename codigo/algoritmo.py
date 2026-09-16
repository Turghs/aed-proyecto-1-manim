from manim import *

def mostrar_algoritmo(self):
    texto = Text(
        "Por definir",
        font_size=30
    )

    self.play(Write(texto))
    self.wait(3)
    self.play(FadeOut(texto))