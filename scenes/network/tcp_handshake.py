from manim import *
from components.default import *


class TCPHandshakeV2(Scene):
    def construct(self):
        apply_theme(self)
        header = SectionHeader(
                "TCP Handshake:", kicker="Module 03 · Networking",
            subtitle="Transmission Control Protocol - Handshake",
        ).to_corner(UL, buff=0.7)
        self.play(FadeIn(header, shift=0.3 * DOWN))

        self.wait(0.5)
        self.play(FadeOut(header))
        # --- Client and Server nodes ---
        client = device(LapTopIcon, "Client")
        server = device(ServerIcon, "Server")
        client.to_edge(LEFT, buff=1.5).shift(UP * 1.5)
        server.to_edge(RIGHT, buff=1.5).shift(UP * 1.5)
        self.play(FadeIn(client), FadeIn(server))
        self.wait(0.5)

        # --- Lifelines ---
        lifeline_length = 4.5
        client_line = DashedLine(
            client.get_bottom(),
            client.get_bottom() + DOWN * lifeline_length,
            color=ACCENT_DIM,
            stroke_width=2,
        )
        server_line = DashedLine(
            server.get_bottom(),
            server.get_bottom() + DOWN * lifeline_length,
            color=ACCENT_DIM,
            stroke_width=2,
        )
        self.play(Create(client_line), Create(server_line))
        self.wait(0.5)

        # Helper to build a small annotation line under a step label
        def annotation(text):
            return SmallText(text, color=TEXT_SECONDARY).scale(0.75)

        # --- Step 1: SYN (client -> server) ---
        y1 = client.get_bottom()[1] - 1.0
        start1 = np.array([client.get_center()[0], y1, 0])
        end1 = np.array([server.get_center()[0], y1, 0])

        step1_label = SmallText("Step 1: Client initiates connection", color=TEXT_SECONDARY)
        #step1_label.next_to(title, DOWN, buff=0.3)
        step1_note = annotation("SYN = 'synchronize' - a request to open a connection and agree on a starting sequence number")
        step1_note.next_to(step1_label, DOWN, buff=0.15)

        syn_packet = Packet("SYN", color=ACCENT_BRIGHT)
        syn_packet.move_to(start1)
        syn_arrow = Connector(start1, end1, label="SYN (seq=x)", color=ACCENT_BRIGHT)

        self.play(FadeIn(step1_label))
        self.play(FadeIn(step1_note))
        self.wait(0.5)
        self.play(FadeIn(syn_packet))
        self.play(
            syn_packet.animate.move_to(end1),
            Create(syn_arrow),
            run_time=1.8,
        )
        self.play(FadeOut(syn_packet))
        self.wait(1.0)

        # --- Step 2: SYN-ACK (server -> client) ---
        y2 = y1 - 1.0
        start2 = np.array([server.get_center()[0], y2, 0])
        end2 = np.array([client.get_center()[0], y2, 0])

        step2_label = SmallText("Step 2: Server acknowledges and responds", color=TEXT_SECONDARY)
        step2_label.move_to(step1_label)
        step2_note = annotation("SYN-ACK = server acknowledges the client's SYN , and sends its own SYN back")
        step2_note.next_to(step2_label, DOWN, buff=0.15)

        synack_packet = Packet("SYN-ACK", color=COLOR_WARNING)
        synack_packet.move_to(start2)
        synack_arrow = Connector(start2, end2, label="SYN-ACK (seq=y, ack=x+1)", color=COLOR_WARNING)

        self.play(FadeOut(step1_note))
        self.play(ReplacementTransform(step1_label, step2_label))
        self.play(FadeIn(step2_note))
        self.wait(0.5)
        self.play(FadeIn(synack_packet))
        self.play(
            synack_packet.animate.move_to(end2),
            Create(synack_arrow),
            run_time=1.8,
        )
        self.play(FadeOut(synack_packet))
        self.wait(1.0)

        # --- Step 3: ACK (client -> server) ---
        y3 = y2 - 1.0
        start3 = np.array([client.get_center()[0], y3, 0])
        end3 = np.array([server.get_center()[0], y3, 0])

        step3_label = SmallText("Step 3: Client confirms — connection established", color=TEXT_SECONDARY)
        step3_label.move_to(step1_label)
        step3_note = annotation("ACK = 'acknowledge' - confirms receipt of the server's SYN; both sides are now synced")
        step3_note.next_to(step3_label, DOWN, buff=0.15)

        ack_packet = Packet("ACK", color=COLOR_SAFE)
        ack_packet.move_to(start3)
        ack_arrow = Connector(start3, end3, label="ACK (ack=y+1)", color=COLOR_SAFE)

        self.play(FadeOut(step2_note))
        self.play(ReplacementTransform(step2_label, step3_label))
        self.play(FadeIn(step3_note))
        self.wait(0.5)
        self.play(FadeIn(ack_packet))
        self.play(
            ack_packet.animate.move_to(end3),
            Create(ack_arrow),
            run_time=1.8,
        )
        self.play(FadeOut(ack_packet))
        self.wait(1.0)

        # --- Connection established ---
        established = MediumText("Connection Established", color=COLOR_SAFE)
        established.next_to(VGroup(client_line, server_line), DOWN, buff=0)

        self.play(FadeOut(step3_note))
        self.play(FadeOut(step3_label))
        self.play(Write(established))
        self.wait(2.0)
