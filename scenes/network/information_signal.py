from manim import *
from components.default import *


class InformationAndSignal(CyberScene):
    """Physical layer: bits → voltage → analog reality → carrier riding."""

    BITS = "10110010"

    def construct(self):
        header = SectionHeader(
            "Information & Signal", kicker="Module 02 · Physical Layer",
            subtitle="From bits to physics",
        ).to_corner(UL, buff=0.7)
        self.play(FadeIn(header, shift=0.3 * DOWN))

        caption = Caption("Your bits are perfect. Physics isn't.")
        self.play(FadeIn(caption))
        self.wait(1)

        def say(text):
            nonlocal caption
            new = Caption(text)
            self.play(FadeTransform(caption, new), run_time=0.7)
            caption = new
            self.wait(2) # increase for more time to read

        # ---- Beat 1 · Information vs Signal ---------------------------
        card_info = InfoCard(
            "Information — the message",
            "Ideas, text, numbers. Abstract, perfect, endlessly copyable.",
            width=5.4)
        card_sig = InfoCard(
            "Signal — the messenger",
            "Voltage on copper, light in fiber, radio in air. "
            "Physical, noisy, real.",
            width=5.4)
        cards = VGroup(card_info, card_sig).arrange(RIGHT, buff=0.8)
        cards.next_to(header, DOWN, buff=0.6)
        cards.move_to(RIGHT * 0.2) # moveed to right
        self.play(FadeIn(cards, lag_ratio=0.15))
        say("A message is information — abstract and perfect. "
            "To send it, it must become a signal: physics.")
        self.play(FadeOut(cards))

        # ---- Beat 2 · Bits become voltage (NRZ) -----------------------
        say("Take these bits. How do they become a wire?")

        big_bits = CodeText(self.BITS, color=ACCENT_BRIGHT).scale(1.6)
        self.play(FadeIn(big_bits, scale=0.8))

        scope = Scope(width=10, height=2.8, title="digital — NRZ")
        scope.move_to(DOWN * 0.6)
        wave = BitWave(self.BITS, width=9, amplitude=0.8)
        wave.move_to(scope.body.get_center())
        row = BitRow(self.BITS, cell=9 / 8)
        row.move_to(wave.get_left() + RIGHT * (wave.width / 2) + UP * 1.05)

        self.play(FadeIn(scope, shift=0.2 * UP))
        self.play(FadeTransform(big_bits, row))
        self.play(Create(wave), run_time=2)
        self.play(*[c.animate.set_color(ACCENT_BRIGHT)
                    for c, b in zip(row, self.BITS) if b == "1"],
                  run_time=0.6)

        cy = scope.body.get_center()[1]
        lbl1 = SmallText("1 = +V", color=ACCENT_BRIGHT)
        lbl1.next_to(scope, RIGHT, buff=0.3).set_y(cy + 0.8)
        lbl0 = SmallText("0 = -V", color=TEXT_SECONDARY)
        lbl0.next_to(scope, RIGHT, buff=0.3).set_y(cy - 0.8)
        self.play(FadeIn(lbl1), FadeIn(lbl0))
        say("1 voltage=bit: high=1,low=0. This is "
            "baseband—the signal sits at low frequency and goes "
            "straight onto the wire.") # its too long to fit on screen
        self.wait(0.5)
        self.play(FadeOut(scope), FadeOut(wave), FadeOut(row),
                  FadeOut(lbl1), FadeOut(lbl0))

        # ---- Beat 3 · Analog, and the big morph -----------------------
        scope = Scope(width=10, height=2.8, title="analog — continuous")
        scope.move_to(DOWN * 0.6)
        self.play(FadeIn(scope, shift=0.2 * UP))

        voice_fn = lambda t: (0.55 * np.sin(TAU * 2.2 * t)
                              + 0.22 * np.sin(TAU * 5.7 * t + 0.9)
                              + 0.15 * np.sin(TAU * 9.3 * t + 2.1))
        voice = WaveCurve(voice_fn, width=9, amplitude=0.7)
        voice.move_to(scope.body.get_center())
        self.play(Create(voice), run_time=1.5)
        say("Analog is continuous: any value, at every instant. Your voice "
            "on a phone line is a voltage wave shaped like this.")
        self.wait(2)

        def square_partial(n, cycles=2.0):
            def fn(t):
                return 4 / PI * sum(np.sin(k * TAU * cycles * t) / k
                                    for k in range(1, n + 1, 2))
            return fn

        sine = WaveCurve(square_partial(1), width=9, amplitude=0.7)
        sine.move_to(scope.body.get_center())
        say("Strip it to the simplest analog wave — a sine.")
        self.play(FadeTransform(voice, sine))

        say("Now the secret about digital: a square wave is just a "
            "recipe of sine waves. Add the odd harmonics and watch.")
        for n in (3, 5, 9, 17):
            target = WaveCurve(square_partial(n), width=9, amplitude=0.7)
            target.move_to(scope.body.get_center())
            self.play(Transform(sine, target), run_time=1.1)

        badge = Badge("DIGITAL = ANALOG, SUMMED", kind="info").to_corner(UR, buff=0.7)
        self.play(FadeIn(badge, scale=0.8))
        say("Odd harmonics stack into a square. Digital signals are built "
            "out of analog physics") # too long
        self.wait(1)
        self.play(FadeOut(scope), FadeOut(sine), FadeOut(badge))

        # ---- Beat 4 · Baseband vs passband ----------------------------
        say("Baseband is fine on a wire. But radio can't carry it — so the "
            "data has to ride a carrier.")

        s1 = Scope(width=9.6, height=1.75, title="baseband — the bits") # its overlaping the tittle
        s2 = Scope(width=9.6, height=1.75, title="carrier — pure sine at f_c")
        s3 = Scope(width=9.6, height=1.75, title="passband — data x carrier")
        stack = VGroup(s1, s2, s3).arrange(DOWN, buff=0.42)
        stack.move_to(DOWN * 0.35)
        self.play(FadeIn(stack, lag_ratio=0.1))

        base = BitWave(self.BITS, width=8.8, amplitude=0.42)
        base.move_to(s1.body.get_center())
        self.play(Create(base), run_time=1.2)

        carrier = SineWave(width=8.8, cycles=26, amplitude=0.42)
        carrier.move_to(s2.body.get_center())
        self.play(Create(carrier), run_time=1.2)

        def ook_fn(bits, cycles=26.0):
            n = len(bits)
            def fn(t):
                i = min(int(t * n), n - 1)
                env = 1.0 if bits[i] == "1" else 0.0
                return env * np.sin(TAU * cycles * t)
            return fn

        ook = WaveCurve(ook_fn(self.BITS), width=8.8, amplitude=0.42,
                        samples=2400)
        ook.move_to(s3.body.get_center())

        say("Multiply them together:")
        ghost = carrier.copy()
        self.play(ghost.animate.move_to(s3.body.get_center()), run_time=0.7)
        self.play(Transform(ghost, ook), run_time=1.4)
        say("…carrier ON for a 1, OFF for a 0. The data now lives in a "
            "band around f_c — that's passband.")
        self.wait(2)
        say("Every radio you own works this way — and different users ride "
            "different carriers, sharing the air without colliding.")
        self.wait(2)
        self.play(FadeOut(stack), FadeOut(base), FadeOut(carrier),
                  FadeOut(ghost))

        # ---- Beat 5 · Bits per symbol ---------------------------------
        say("One last trick: a symbol can carry several bits.")

        scope = Scope(width=10, height=2.8, title="4-level — 2 bits per symbol")
        scope.move_to(DOWN * 0.5)
        self.play(FadeIn(scope, shift=0.2 * UP))

        level_map = {"00": -1.0, "01": -0.34, "11": 0.34, "10": 1.0}
        symbols = ["00", "01", "11", "10", "01", "11", "00", "10"]
        cx, cy = scope.body.get_center()[:2]

        refs = VGroup()
        for s, v in level_map.items():
            y = cy + 0.78 * v
            line = DashedLine([cx - 4.4, y, 0], [cx + 4.4, y, 0],
                              color=ACCENT_DIM, stroke_width=1.5)
            lbl = CodeText(s, color=TEXT_SECONDARY).scale(0.7)
            lbl.next_to(line, LEFT, buff=0.15)
            refs.add(VGroup(line, lbl))
        self.play(FadeIn(refs, lag_ratio=0.1))

        pam = LevelWave([level_map[s] for s in symbols],
                        width=9, amplitude=0.78)
        pam.move_to(scope.body.get_center())
        self.play(Create(pam), run_time=1.8)

        sym_row = VGroup()
        for i, s in enumerate(symbols):
            t = CodeText(s, color=TEXT_SECONDARY).scale(0.75)
            t.move_to(np.array([cx - 4.5 + (i + 0.5) * (9 / 8), cy + 1.05, 0]))
            sym_row.add(t)
        self.play(FadeIn(sym_row, lag_ratio=0.08))

        say("Four levels means two bits per step — same wave speed, "
            "double the data.")
        self.wait(1)
        say("Modern Wi-Fi pushes this to 1024 levels: ten bits "
            "in a single symbol.")
        self.wait(0.5)

        # ---- Beat 6 · Security outro ----------------------------------
        self.play(FadeOut(scope), FadeOut(refs), FadeOut(pam),
                  FadeOut(sym_row))
        say("So why does a hacker care about any of this?")

        final = VGroup(
            MediumText("Your secrets are bits."),
            MediumText("Bits become voltage, light, and radio."),
            MediumText("And physics can be measured.", color=COLOR_DANGER),
        ).arrange(DOWN, buff=0.4)
        self.play(FadeOut(caption), FadeIn(final, shift=0.3 * UP))

        self.wait(2)
