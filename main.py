from manim import *

from codigo.intro import mostrar_intro
from codigo.explicacion import mostrar_explicacion
from codigo.algoritmo import mostrar_algoritmo
from codigo.cierre import mostrar_cierre


class ProyectoCompleto(Scene):
    def construct(self):
        mostrar_intro(self)
        mostrar_explicacion(self)
        mostrar_algoritmo(self)
        mostrar_cierre(self)