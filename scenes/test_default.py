from manim import *
from components.default import *


class TestDefault(Scene):
    def construct(self):
        apply_theme(self)

        title = Title("Cybersecurity Visual System")
        title.to_edge(UP)

        heading = Heading("Typography & Panels")
        heading.next_to(title, DOWN, buff=0.4)

        self.play(Write(title))
        self.play(FadeIn(heading, shift=UP * 0.2))
        self.wait(0.5)

        large = LargeText("Large text — key concepts")
        medium = MediumText("Medium text — general explanation")
        small = SmallText("Small text — captions & labels")
        code = CodeText("GET /index.html HTTP/1.1")

        text_group = VGroup(large, medium, small, code).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        text_group.next_to(heading, DOWN, buff=0.6).to_edge(LEFT, buff=1.0)

        self.play(LaggedStart(
            *[FadeIn(t, shift=UP * 0.1) for t in text_group],
            lag_ratio=0.2
        ))
        self.wait(0.5)

        small_box = SmallBox()
        medium_box = MediumBox()
        large_box = LargeBox()

        box_group = VGroup(small_box, medium_box, large_box).arrange(DOWN, buff=0.3)
        box_group.next_to(text_group, RIGHT, buff=1.2)

        small_label = SmallText("Small").move_to(small_box)
        medium_label = SmallText("Medium").move_to(medium_box)
        large_label = SmallText("Large").move_to(large_box)

        self.play(
            LaggedStart(
                *[Create(b) for b in box_group],
                lag_ratio=0.2
            )
        )
        self.play(
            FadeIn(small_label),
            FadeIn(medium_label),
            FadeIn(large_label),
        )
        self.wait(0.5)

        # Semantic color demo
        safe = SmallBox(stroke_color=COLOR_SAFE, fill_color=COLOR_SAFE)
        warn = SmallBox(stroke_color=COLOR_WARNING, fill_color=COLOR_WARNING)
        danger = SmallBox(stroke_color=COLOR_DANGER, fill_color=COLOR_DANGER)

        semantic_group = VGroup(safe, warn, danger).arrange(RIGHT, buff=0.4)
        semantic_group.next_to(box_group, DOWN, buff=0.8).align_to(box_group, LEFT)

        safe_label = SmallText("Safe").next_to(safe, DOWN, buff=0.15)
        warn_label = SmallText("Warning").next_to(warn, DOWN, buff=0.15)
        danger_label = SmallText("Danger").next_to(danger, DOWN, buff=0.15)

        self.play(
            LaggedStart(
                *[Create(b) for b in semantic_group],
                lag_ratio=0.2
            )
        )
        self.play(
            FadeIn(safe_label),
            FadeIn(warn_label),
            FadeIn(danger_label),
        )
        self.wait(1)
