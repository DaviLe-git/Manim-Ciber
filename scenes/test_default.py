from manim import *
from components.default import *


class TestDefault(Scene):
    def construct(self):

        title = Title("Cybersecurity Animation")
        title.to_edge(UP)

        heading = Heading("Typography")
        heading.next_to(title, DOWN, buff=0.5)

        large = LargeText("Large Text")
        medium = MediumText("Medium Text")
        small = SmallText("Small Text")

        large.next_to(heading, DOWN, buff=0.5)
        medium.next_to(large, DOWN, buff=0.3)
        small.next_to(medium, DOWN, buff=0.3)

        small_box = SmallBox()
        medium_box = MediumBox()
        large_box = LargeBox()

        small_box.move_to(LEFT * 4 + DOWN * 2)
        medium_box.move_to(DOWN * 2)
        large_box.move_to(RIGHT * 3 + DOWN * 2)

        self.play(
            Write(title),
            Write(heading),
        )

        self.play(
            Write(large),
            Write(medium),
            Write(small),
        )

        self.play(
            Create(small_box),
            Create(medium_box),
            Create(large_box),
        )

        self.wait(2)
