from manim import *
from components.default import *

class TCPIP(Scene):
    def construct(self):
        apply_theme(self)
        title = Title("TCP/IP Protocol")
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)
