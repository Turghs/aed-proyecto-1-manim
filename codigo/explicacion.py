from manim import *

def mostrar_explicacion(self):
    texto = Text(
        "Por definir",
        font_size=28
    )

    self.play(Write(texto))
    self.wait(3)
    self.play(FadeOut(texto))