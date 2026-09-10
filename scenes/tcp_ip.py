from manim import *
from components.default import *


class TCPIP(CyberScene):

    def construct(self):
        header = SectionHeader(
            "TCP/IP", kicker="Module 01 · Networking",
            subtitle="Two protocols, one job",
        ).to_corner(UL, buff=0.7)
        self.play(FadeIn(header, shift=0.3 * DOWN))

        caption = Caption("TCP/IP isn't one protocol — it's two, splitting the work.")
        self.play(FadeIn(caption))

        def say(text):
            nonlocal caption
            new = Caption(text)
            self.play(FadeTransform(caption, new), run_time=0.7)
            caption = new

        card_ip = InfoCard(
            "IP — the postal service",
            "Addresses each packet and routes it hop by hop. "
            "Best-effort only: it may lose or shuffle them.",
            width=5.4,
        )
        card_tcp = InfoCard(
            "TCP — the paperwork",
            "Numbers every byte, waits for a receipt (ACK), "
            "and resends anything that goes missing.",
            width=5.4,
        )
        cards = VGroup(card_ip, card_tcp).arrange(RIGHT, buff=1.0)
        cards.next_to(header, DOWN, buff=0.6)
        cards.move_to(RIGHT * 0.2)

        self.play(FadeIn(cards, lag_ratio=0.15))
        self.wait(1)

        say("Now watch the two of them work together.")
        self.play(FadeOut(cards))

        def device(icon_fn, name, color=ACCENT):
            return VGroup(icon_fn(color=color), SmallText(name)).arrange(DOWN, buff=0.25)

        sender = device(LaptopIcon, "Sender")
        receiver = device(ServerIcon, "Receiver")
        net = VGroup(sender, receiver).arrange(RIGHT, buff=3.8)
        net.move_to(DOWN * 0.4)
        self.play(FadeIn(net, lag_ratio=0.2))

        sr = sender[0].get_right()          
        rl = receiver[0].get_left()

        say("Before any data, both sides must agree to talk.")

        c_syn = Connector(sr + UP * 0.55 + RIGHT * 0.05,
                          rl + UP * 0.55 + LEFT * 0.05, label="SYN")
        p_syn = Packet("SYN", color=ACCENT_BRIGHT)
        path_syn = Line(sr + UP * 0.55 + RIGHT * 0.15,
                        rl + UP * 0.55 + LEFT * 0.15).set_opacity(0)
        p_syn.move_to(path_syn.get_start())
        self.play(Create(c_syn))
        self.play(MoveAlongPath(p_syn, path_syn), run_time=1.2)
        self.play(FadeOut(p_syn, shift=0.2 * RIGHT))
        say("SYN: “I'd like to talk.”")

        c_synack = Connector(rl + LEFT * 0.05, sr + RIGHT * 0.05,
                             label="SYN-ACK", side=DOWN)
        p_synack = Packet("SYN-ACK", color=ACCENT_BRIGHT)
        path_synack = Line(rl + LEFT * 0.15, sr + RIGHT * 0.15).set_opacity(0)
        p_synack.move_to(path_synack.get_start())
        self.play(Create(c_synack))
        self.play(MoveAlongPath(p_synack, path_synack), run_time=1.4)
        self.play(FadeOut(p_synack, shift=0.2 * LEFT))
        say("SYN-ACK: “Agreed — I'm listening.”")

        c_ack = Connector(sr + DOWN * 0.55 + RIGHT * 0.05,
                          rl + DOWN * 0.55 + LEFT * 0.05,
                          label="ACK", side=DOWN)
        p_ack = Packet("ACK", color=ACCENT_BRIGHT)
        path_ack = Line(sr + DOWN * 0.55 + RIGHT * 0.15,
                        rl + DOWN * 0.55 + LEFT * 0.15).set_opacity(0)
        p_ack.move_to(path_ack.get_start())
        self.play(Create(c_ack))
        self.play(MoveAlongPath(p_ack, path_ack), run_time=1.2)
        self.play(FadeOut(p_ack, shift=0.2 * RIGHT))
        say("ACK: “Confirmed.”")

        established = Badge("CONNECTION ESTABLISHED", kind="safe")
        established.move_to((sr + rl) / 2 + UP * 1.5)
        self.play(FadeIn(established, scale=0.8))
        self.wait(0.5)
        self.play(FadeOut(c_syn), FadeOut(c_synack), FadeOut(c_ack))

        say("Every chunk is numbered — and each needs a receipt.")

        d1 = Packet("SEQ = 1").move_to(path_syn.get_start())
        self.play(MoveAlongPath(d1, path_syn), run_time=1.0)
        a1 = Packet("ACK 1", color=COLOR_SAFE).move_to(path_synack.get_start())
        self.play(MoveAlongPath(a1, path_synack), run_time=1.0)
        self.play(FadeOut(d1, shift=0.2 * RIGHT), FadeOut(a1, shift=0.2 * LEFT))

        say("If no receipt comes back in time…")

        d2 = Packet("SEQ = 2").move_to(path_syn.get_start())
        self.play(MoveAlongPath(d2, path_syn), run_time=0.8,
                  rate_func=lambda t: 0.5 * t)         

        lost_at = path_syn.point_from_proportion(0.5)
        lost = SmallText("lost in transit", color=COLOR_WARNING)
        lost.next_to(lost_at, UP, buff=0.25)
        self.play(FadeOut(d2, shift=0.3 * DOWN),
                  FadeIn(lost, shift=0.1 * DOWN),
                  Flash(lost_at, color=COLOR_WARNING, line_length=0.3))
        self.wait(0.5)

        say("…TCP assumes it was lost, and simply sends it again.")
        self.play(FadeOut(lost))

        d2b = Packet("SEQ = 2").move_to(path_syn.get_start())
        self.play(MoveAlongPath(d2b, path_syn), run_time=1.0)
        a2 = Packet("ACK 2", color=COLOR_SAFE).move_to(path_synack.get_start())
        self.play(MoveAlongPath(a2, path_synack), run_time=1.0)
        self.play(FadeOut(d2b, shift=0.2 * RIGHT), FadeOut(a2, shift=0.2 * LEFT))

        say("That's the whole trick:")

        final = VGroup(
            MediumText("IP moves the packets."),
            MediumText("TCP makes sure they arrive.", color=ACCENT_BRIGHT),
        ).arrange(DOWN, buff=0.35)
        self.play(FadeOut(net), FadeOut(established), FadeOut(caption),
                  FadeIn(final, shift=0.3 * UP))
        self.wait(2)
