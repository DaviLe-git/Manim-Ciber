from manim import *
from components.default import *

class TCPIP(Scene):
    def construct(self):
        apply_theme(self)
        title = Title("TCP/IP Protocol")
        title.to_edge(UP)
        self.play(Write(title))

        def device(icon_fn, name, color=ACCENT):
            return VGroup(icon_fn(color=color), SmallText(name)).arrange(DOWN, buff=0.25)

        sender = device(LaptopIcon,"Sender")
        receiver = device(ServerIcon,"Receiver")

        net = VGroup(sender, receiver).arrange(RIGHT, buff=2.4)
        net.next_to(title, DOWN, buff=0.7)
        net.shift(RIGHT)

        
        self.play(Create(sender),Create(receiver))

        self.wait(0.5)
