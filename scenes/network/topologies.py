from itertools import combinations

from manim import *
from components.default import *

STAGE = RIGHT * 0.2 + DOWN * 0.4   # where the diagrams live


class NetworkTopologies(CyberScene):
    """Four topologies, one question: what happens when something breaks?"""

    def construct(self):
        header = SectionHeader(
            "Network Topologies", kicker="Module 03 · Networking",
            subtitle="Four ways to wire a network",
        ).to_corner(UL, buff=0.7)
        self.play(FadeIn(header, shift=0.3 * DOWN))

        caption = Caption("Four shapes — one question: what happens when something breaks?")
        self.play(FadeIn(caption))

        def say(text):
            nonlocal caption
            new = Caption(text)
            self.play(FadeTransform(caption, new), run_time=0.7)
            caption = new

        def badge_for(text, kind):
            return Badge(text, kind=kind).to_corner(UR, buff=0.7)

        def dim(*mobjs):
            self.play(*[m.animate.set_opacity(0.25) for m in mobjs], run_time=0.5)

        # ================= 1 · BUS =================
        badge = badge_for("BUS", kind="danger")
        self.play(FadeIn(badge, scale=0.8))

        bus_y = -0.5
        backbone = Line([-3.2, bus_y, 0], [3.2, bus_y, 0],
                        color=ACCENT, stroke_width=3)
        cable_label = SmallText("one shared cable").next_to(backbone, DOWN, buff=0.15)
        xs = [-2.4, -0.8, 0.8, 2.4]
        nodes = VGroup(*[NetNode(lbl, radius=0.38) for lbl in "ABCD"])
        for node, x in zip(nodes, xs):
            node.move_to([x, bus_y + 1.0, 0])
        drops = VGroup(*[Link([x, bus_y + 0.62, 0], [x, bus_y, 0]) for x in xs])
        bus = VGroup(backbone, drops, nodes, cable_label)

        self.play(FadeIn(backbone), FadeIn(cable_label))
        self.play(LaggedStart(FadeIn(drops),
                              *[FadeIn(n, shift=0.2 * DOWN) for n in nodes],
                              lag_ratio=0.15))

        say("Everyone shares one cable — every machine hears every message.")
        data = Packet("DATA").scale(0.65)
        bus_path = Line([-3.0, bus_y, 0], [3.0, bus_y, 0]).set_opacity(0)
        data.move_to(bus_path.get_start())
        self.play(MoveAlongPath(data, bus_path), run_time=1.6)
        self.play(LaggedStart(*[Indicate(n, color=ACCENT_BRIGHT) for n in nodes],
                              lag_ratio=0.15))
        self.play(FadeOut(data))

        say("But one cut takes the whole network down. Bus is history.")
        cut = FailMark([0, bus_y, 0], size=0.5)
        self.play(Create(cut), Flash([0, bus_y, 0], color=COLOR_DANGER, line_length=0.3))
        dim(backbone, drops, nodes, cable_label)
        self.play(FadeOut(bus), FadeOut(cut), FadeOut(badge))

        # ================= 2 · RING =================
        badge = badge_for("RING", kind="warning")
        self.play(FadeIn(badge, scale=0.8))

        ring_pos = circular_layout("ABCDE", radius=1.35, center=STAGE)
        ring = GraphDiagram(ring_pos, [("A", "B"), ("B", "C"), ("C", "D"),
                                       ("D", "E"), ("E", "A")])
        self.play(FadeIn(ring, lag_ratio=0.08))

        say("A circle: data hops machine to machine around the loop.")
        token = Packet("TOKEN").scale(0.55)
        for a, b in [("A", "B"), ("B", "C")]:
            link = ring.links[(a, b)]
            token.move_to(link.get_start())
            self.play(MoveAlongPath(token, link), run_time=0.7)

        say("One dead node breaks the loop — data can't get past it.")
        dead, fail = ring.nodes["C"], FailMark(ring.nodes["C"])
        self.play(Create(fail),
                  Flash(dead.get_center(), color=COLOR_DANGER, line_length=0.35))
        dim(dead, ring.links[("B", "C")], ring.links[("C", "D")])
        self.play(Indicate(token, color=COLOR_WARNING))
        self.play(FadeOut(token), FadeOut(ring), FadeOut(fail), FadeOut(badge))

        # ================= 3 · STAR =================
        badge = badge_for("STAR", kind="info")
        self.play(FadeIn(badge, scale=0.8))

        switch = NetNode("SW", radius=0.5, color=ACCENT_BRIGHT).move_to(STAGE)
        icons = [LaptopIcon(), LaptopIcon(), ServerIcon(), PhoneIcon(), LaptopIcon()]
        names = ["laptop", "laptop", "server", "phone", "laptop"]
        spots = circular_layout(list(range(5)), radius=2.0, center=STAGE)
        devices = VGroup()
        for i, (icon, name) in enumerate(zip(icons, names)):
            d = VGroup(icon, SmallText(name)).arrange(DOWN, buff=0.2)
            d.move_to(spots[i])
            devices.add(d)
        spokes = VGroup(*[
            Link(edge_toward(switch, d.get_center()),
                 edge_toward(d, switch.get_center()))
            for d in devices
        ])
        star = VGroup(spokes, switch, devices)

        self.play(FadeIn(spokes), FadeIn(switch, scale=0.8),
                  LaggedStart(*[FadeIn(d, shift=0.2 * UP) for d in devices],
                              lag_ratio=0.1))

        say("One central switch, one cable per device — today's standard.")
        say("A dead cable costs one machine. A dead switch costs everything.")

        cut1 = FailMark(spokes[0].get_center(), size=0.4)
        self.play(Create(cut1),
                  Flash(spokes[0].get_center(), color=COLOR_WARNING, line_length=0.3))
        dim(devices[0], spokes[0])

        hub_fail = FailMark(switch, size=0.9)
        self.play(Create(hub_fail),
                  Flash(switch.get_center(), color=COLOR_DANGER, line_length=0.4))
        dim(switch, spokes, devices)
        self.play(FadeOut(star), FadeOut(cut1), FadeOut(hub_fail), FadeOut(badge))

        # ================= 4 · MESH =================
        badge = badge_for("MESH", kind="safe")
        self.play(FadeIn(badge, scale=0.8))

        mesh_pos = circular_layout("ABCDEF", radius=1.5, center=STAGE)
        mesh = GraphDiagram(mesh_pos, list(combinations("ABCDEF", 2)))
        self.play(FadeIn(mesh, lag_ratio=0.03))

        say("Everyone connects to everyone — traffic picks any path.")
        def leg(a, b):
            return Link(mesh_pos[a], mesh_pos[b],
                        color=ACCENT_BRIGHT, stroke_width=4, trim=0.45)

        route1 = VGroup(leg("A", "C"), leg("C", "D"))
        self.play(Create(route1))
        msg = Packet("DATA").scale(0.6).move_to(route1[0].get_start())
        self.play(MoveAlongPath(msg, route1[0]), run_time=0.8)
        self.play(MoveAlongPath(msg, route1[1]), run_time=0.8)

        say("Now a node dies mid-route…")
        dead, fail = mesh.nodes["C"], FailMark(mesh.nodes["C"])
        self.play(FadeOut(msg), FadeOut(route1), Create(fail),
                  Flash(dead.get_center(), color=COLOR_DANGER, line_length=0.35))
        dim(dead, *[mesh.links[("C", x)] for x in "ABDEF"])

        say("…and traffic simply routes around the damage. This is the Internet.")
        route2 = VGroup(leg("A", "F"), leg("F", "E"), leg("E", "D"))
        self.play(Create(route2))
        msg2 = Packet("DATA").scale(0.6).move_to(route2[0].get_start())
        for l in route2:
            self.play(MoveAlongPath(msg2, l), run_time=0.7)
        self.play(FadeOut(msg2, shift=0.2 * RIGHT))

        say("The price: full mesh needs n(n − 1)/2 links — six nodes, fifteen cables.")
        self.play(FadeOut(mesh), FadeOut(route2), FadeOut(fail), FadeOut(badge))

        # ================= 5 · WHO WINS? =================
        say("So which one do you actually use?")
        verdicts = [
            ("BUS", "one cut kills everyone", "danger"),
            ("RING", "one node stops the loop", "warning"),
            ("STAR", "a dead hub kills everyone", "warning"),
            ("MESH", "routes around failure", "safe"),
        ]
        grid = VGroup(*[
            LabeledBox(f"{n} — {t}", box_size="small", width=4.6,
                       stroke_color=SEMANTIC_COLORS[k])
            for n, t, k in verdicts
        ]).arrange_in_grid(rows=2, cols=2, buff=0.5)
        grid.move_to(DOWN * 0.2)
        self.play(FadeIn(grid, lag_ratio=0.15))
        self.wait(1)

        final = VGroup(
            MediumText("Every topology is a bet on what fails first."),
            MediumText("The Internet bet on mesh.", color=ACCENT_BRIGHT),
        ).arrange(DOWN, buff=0.35)
        self.play(FadeOut(grid), FadeOut(caption),
                  FadeIn(final, shift=0.3 * UP))
        self.wait(2)
