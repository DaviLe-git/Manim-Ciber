from manim import *


class WebsiteRequest(Scene):
    def construct(self):

        title = Text("What happens when you visit a website?")

        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))
