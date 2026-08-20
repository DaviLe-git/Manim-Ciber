"""
scenes/test_default.py — visual test-suite for components/default.py

Render a single family:
    manim -pql scenes/test_default.py TestTerminal

Render the whole suite:
    manim -pql -a scenes/test_default.py

Scenes:
    TestTypography    — text helpers at every size + full color palette
    TestPanels        — Small/Medium/Large boxes, LabeledBox, Panel
    TestBadges        — status pills for every semantic kind
    TestIcons         — device/security icons (color variants too)
    TestTerminal      — Terminal window, add_line(), TypeIn()
    TestDiagram       — Connectors (solid/dashed), travelling Packets
    TestCompositions  — InfoCard, BulletList, Divider, Caption

SectionHeader is exercised at the top of every scene as a bonus.
"""

from manim import *
from components.default import *


# ============================================================
# 01 · TYPOGRAPHY + PALETTE
# ============================================================

class TestTypography(CyberScene):
    def construct(self):
        header = SectionHeader(
            "Typography", kicker="01 · Text",
            subtitle="Every helper, every size",
        ).to_corner(UL, buff=0.7)
        self.play(FadeIn(header, shift=0.3 * DOWN))

        rows = VGroup(
            LargeText("Large — key concepts"),
            MediumText("Medium — general explanation"),
            SmallText("Small — captions & labels"),
            CodeText("$ nmap -sV 10.0.0.5"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        rows.next_to(header, DOWN, buff=0.8).align_to(header, LEFT)

        self.play(LaggedStart(
            *[FadeIn(r, shift=0.2 * RIGHT) for r in rows],
            lag_ratio=0.25,
        ))

        def swatch_row(name, color):
            chip = RoundedRectangle(
                width=0.34, height=0.34, corner_radius=0.08,
                fill_color=color, fill_opacity=1,
                stroke_color=ACCENT_DIM, stroke_width=1,
            )
            label = SmallText(name).scale(0.75)
            return VGroup(chip, label).arrange(RIGHT, buff=0.25)

        col_a = VGroup(*[swatch_row(n, c) for n, c in [
            ("ACCENT", ACCENT),
            ("ACCENT_BRIGHT", ACCENT_BRIGHT),
            ("ACCENT_DIM", ACCENT_DIM),
            ("PANEL_BACKGROUND", PANEL_BACKGROUND),
        ]]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)

        col_b = VGroup(*[swatch_row(n, c) for n, c in [
            ("TEXT_PRIMARY", TEXT_PRIMARY),
            ("TEXT_SECONDARY", TEXT_SECONDARY),
            ("COLOR_SAFE", COLOR_SAFE),
            ("COLOR_WARNING", COLOR_WARNING),
            ("COLOR_DANGER", COLOR_DANGER),
        ]]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)

        palette = VGroup(col_a, col_b).arrange(RIGHT, aligned_edge=TOP, buff=1.0)
        palette.next_to(rows, RIGHT, buff=1.2).align_to(rows, UP)

        self.play(FadeIn(palette, lag_ratio=0.05))
        self.wait()


# ============================================================
# 02 · PANELS & BOXES
# ============================================================

class TestPanels(CyberScene):
    def construct(self):
        header = SectionHeader(
            "Panels & Boxes", kicker="02 · Containers",
        ).to_corner(UL, buff=0.7)
        self.play(FadeIn(header, shift=0.3 * DOWN))

        sizes = VGroup(
            LabeledBox("Small", box_size="small"),
            LabeledBox("Medium", box_size="medium"),
            LabeledBox("Large", box_size="large"),
        ).arrange(RIGHT, buff=0.6)

        semantic = VGroup(
            LabeledBox("SAFE", box_size="medium", stroke_color=COLOR_SAFE),
            LabeledBox("WARNING", box_size="medium", stroke_color=COLOR_WARNING),
            LabeledBox("DANGER", box_size="medium", stroke_color=COLOR_DANGER),
        ).arrange(RIGHT, buff=0.6)

        heavy = Panel(2.2, 1.0, COLOR_DANGER, fill_opacity=0.3)
        heavy_label = SmallText("heavier fill").move_to(heavy)

        custom = VGroup(
            LabeledBox("3.6 × 1.0 custom", width=3.6, height=1.0,
                       stroke_color=ACCENT_BRIGHT),
            LabeledBox("A very long label that auto-shrinks", width=2.4, height=0.9),
            VGroup(heavy, heavy_label),
        ).arrange(RIGHT, buff=0.6)

        rows = VGroup(sizes, semantic, custom).arrange(DOWN, buff=0.55,
                                                       aligned_edge=LEFT)
        rows.next_to(header, DOWN, buff=0.7).align_to(header, LEFT)

        boxes = [item[0] for row in (sizes, semantic, custom) for item in row]
        labels = [item[1] for row in (sizes, semantic, custom) for item in row]

        self.play(LaggedStart(*[Create(b) for b in boxes], lag_ratio=0.12))
        self.play(FadeIn(VGroup(*labels), lag_ratio=0.1))
        self.wait()


# ============================================================
# 03 · BADGES
# ============================================================

class TestBadges(CyberScene):
    def construct(self):
        header = SectionHeader("Badges", kicker="03 · Status").to_corner(UL, buff=0.7)
        self.play(FadeIn(header, shift=0.3 * DOWN))

        rows = VGroup()
        for kind in ("info", "safe", "warning", "danger", "neutral"):
            badge = Badge(kind.upper(), kind=kind)
            snippet = CodeText(f'Badge("{kind}")',
                               color=TEXT_SECONDARY).scale(0.65)
            rows.add(VGroup(badge, snippet).arrange(RIGHT, buff=0.7))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        rows.next_to(header, DOWN, buff=0.8).align_to(header, LEFT)

        mini = Badge("ENCRYPTED", kind="safe", font_size=SMALL_TEXT_SIZE * 0.7)
        mini.next_to(rows, RIGHT, buff=1.4).align_to(rows, UP)

        self.play(FadeIn(rows, lag_ratio=0.1), FadeIn(mini))
        self.play(Indicate(rows[3][0], scale_factor=1.15, color=COLOR_DANGER))
        self.wait()


# ============================================================
# 04 · ICONS
# ============================================================

class TestIcons(CyberScene):
    def construct(self):
        header = SectionHeader(
            "Icons", kicker="04 · Devices & security",
        ).to_corner(UL, buff=0.7)
        self.play(FadeIn(header, shift=0.3 * DOWN))

        def cell(icon, name):
            return VGroup(icon, SmallText(name)).arrange(DOWN, buff=0.3)

        grid = VGroup(
            cell(LaptopIcon(), "LaptopIcon"),
            cell(ServerIcon(), "ServerIcon"),
            cell(PhoneIcon(), "PhoneIcon"),
            cell(LockIcon(), "LockIcon"),
            cell(LockIcon(COLOR_WARNING), "recolorable"),
            cell(ShieldIcon(), "ShieldIcon"),
            cell(ShieldIcon(checked=True), "ShieldIcon(checked)"),
            cell(FirewallIcon(color=COLOR_DANGER), "FirewallIcon"),
        ).arrange_in_grid(rows=2, cols=4, buff=0.8)

        grid.next_to(header, DOWN, buff=0.6)

        self.play(LaggedStart(
            *[FadeIn(c, shift=0.2 * UP, scale=0.9) for c in grid],
            lag_ratio=0.12,
        ))
        self.wait()


# ============================================================
# 05 · TERMINAL
# ============================================================

class TestTerminal(CyberScene):
    def construct(self):
        header = SectionHeader("Terminal", kicker="05 · CLI mock").to_corner(UL, buff=0.7)
        self.play(FadeIn(header, shift=0.3 * DOWN))

        term = Terminal(
            lines=[
                ("$ nmap -sV 10.0.0.5", ACCENT_BRIGHT),
                ("Starting Nmap 7.94 — https://nmap.org", TEXT_SECONDARY),
            ],
            title="analyst@soc: ~",
            width=8.2,
            height=3.6,   # reserve room for lines added later
        ).next_to(header, DOWN, buff=0.6).align_to(header, LEFT)

        # Fade in window chrome, then type the seeded lines
        self.play(FadeIn(term[:4], shift=0.3 * UP))
        for line in term.lines:
            self.play(TypeIn(line), run_time=1.0)

        # Lines appended at runtime (mix of plain + colored tuples)
        for line in ("22/tcp   open  ssh",
                     "443/tcp  open  https",
                     "21/tcp   open  ftp",
                     ("[!] vsftpd 2.3.4 — known backdoor", COLOR_DANGER)):
            self.play(TypeIn(term.add_line(line)), run_time=0.9)

        self.play(Circumscribe(term.lines[-1], color=COLOR_DANGER))

        alert = VGroup(
            Badge("CRITICAL FINDING", kind="danger"),
            InfoCard("Mitigation",
                     "Remove vsftpd 2.3.4 or upgrade to a patched release.",
                     width=3.6),
        ).arrange(DOWN, buff=0.5)
        alert.next_to(term, RIGHT, buff=0.8).align_to(term, UP)

        self.play(FadeIn(alert, shift=0.2 * LEFT))
        self.wait()


# ============================================================
# 06 · CONNECTORS & PACKETS (mini network diagram)
# ============================================================

class TestDiagram(CyberScene):
    def construct(self):
        header = SectionHeader(
            "Connectors & Packets", kicker="06 · Data flow",
        ).to_corner(UL, buff=0.7)
        self.play(FadeIn(header, shift=0.3 * DOWN))

        def device(icon_fn, name, color=ACCENT):
            return VGroup(icon_fn(color=color), SmallText(name)).arrange(DOWN, buff=0.25)

        client = device(LaptopIcon, "Client")
        firewall = device(FirewallIcon, "Firewall")
        server = device(ServerIcon, "Server")

        net = VGroup(client, firewall, server).arrange(RIGHT, buff=2.4)
        net.next_to(header, DOWN, buff=0.7)

        c_req = Connector(
            client[0].get_right() + RIGHT * 0.05,
            firewall[0].get_left() + LEFT * 0.05,
            label="HTTPS request",
        )
        c_ok = Connector(
            firewall[0].get_right() + RIGHT * 0.05,
            server[0].get_left() + LEFT * 0.05,
            label="allowed", color=COLOR_SAFE,
        )

        self.play(LaggedStart(
            *[FadeIn(d, shift=0.2 * UP) for d in net], lag_ratio=0.15,
        ))
        self.play(Create(c_req), Create(c_ok))

        # Dashed danger connector: attacker gets blocked below
        attacker = device(LaptopIcon, "Attacker", color=COLOR_DANGER)
        attacker.next_to(firewall, DOWN, buff=1.2)

        c_block = Connector(
            attacker[0].get_top() + UP * 0.05,
            firewall[0].get_bottom() + DOWN * 0.05,
            label="BLOCKED", color=COLOR_DANGER,
            dashed=True, side=RIGHT,
        )
        self.play(FadeIn(attacker, shift=0.2 * DOWN), Create(c_block))

        # Invisible paths for packets to travel along
        path1 = Line(client[0].get_right() + RIGHT * 0.05,
                     firewall[0].get_left() + LEFT * 0.05).set_opacity(0)
        path2 = Line(firewall[0].get_right() + RIGHT * 0.05,
                     server[0].get_left() + LEFT * 0.05).set_opacity(0)
        path_back = Line(server[0].get_left() + LEFT * 0.05 + UP * 0.55,
                         client[0].get_right() + RIGHT * 0.05 + UP * 0.55).set_opacity(0)
        path_evil = Line(attacker[0].get_top() + UP * 0.05,
                         firewall[0].get_bottom() + DOWN * 0.05).set_opacity(0)

        req = Packet("GET /").move_to(path1.get_start())
        self.play(MoveAlongPath(req, path1), run_time=1.2)
        self.play(FadeOut(req, shift=0.1 * RIGHT))

        req2 = Packet("GET /").move_to(path2.get_start())
        self.play(MoveAlongPath(req2, path2), run_time=1.0)
        self.play(FadeOut(req2, shift=0.1 * RIGHT))

        resp = Packet("200 OK", color=COLOR_SAFE).move_to(path_back.get_start())
        self.play(MoveAlongPath(resp, path_back), run_time=1.6)
        self.play(FadeOut(resp, shift=0.1 * RIGHT))

        evil = Packet("EXPLOIT", color=COLOR_DANGER).move_to(path_evil.get_start())
        self.play(MoveAlongPath(evil, path_evil), run_time=1.0)
        self.play(FadeOut(evil),
                  Flash(firewall[0].get_bottom(), color=COLOR_DANGER, line_length=0.35))
        self.wait()


# ============================================================
# 07 · COMPOSITIONS
# ============================================================

class TestCompositions(CyberScene):
    def construct(self):
        header = SectionHeader(
            "Compositions", kicker="07 · Building blocks",
        ).to_corner(UL, buff=0.7)
        self.play(FadeIn(header, shift=0.3 * DOWN))

        card = InfoCard(
            "Defense in Depth",
            "Layer independent controls so a single failure never exposes the system.",
            width=5.2,
        )
        rule = Divider(4.4)
        left = VGroup(card, rule).arrange(DOWN, buff=0.5)

        dots = BulletList("Network segmentation",
                          "Patch management",
                          "Least privilege", buff=0.25)
        numbered = BulletList("Identify", "Protect", "Detect",
                              marker="number", buff=0.2,
                              font_size=SMALL_TEXT_SIZE * 1.1)
        right = VGroup(dots, numbered).arrange(DOWN, buff=0.6, aligned_edge=LEFT)

        cols = VGroup(left, right).arrange(RIGHT, buff=1.2)
        cols.next_to(header, DOWN, buff=0.7).align_to(header, LEFT)

        caption = Caption("Every component above comes from components/default.py")

        self.play(FadeIn(card, shift=0.2 * UP))
        self.play(Create(rule))
        self.play(FadeIn(dots, lag_ratio=0.1), FadeIn(numbered, lag_ratio=0.1))
        self.play(FadeIn(caption, shift=0.2 * UP))
        self.wait()
