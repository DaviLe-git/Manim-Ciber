"""
default.py — shared visual theme for the cybersecurity video series.

Design language: dark editorial (deep slate background, muted teal accent,
off-white text). All original helpers keep their names and signatures,
so existing scenes keep working — everything new is additive.
"""

from __future__ import annotations

from typing import Optional, Sequence, Tuple, Union

from manim import *

import numpy as np

# ============================================================
# 1 · COLOR PALETTE
# ============================================================

BACKGROUND_COLOR = "#12181F"     # deep slate / near-black navy
PANEL_BACKGROUND = "#1B242E"     # slightly lighter panel background
TERMINAL_BACKGROUND = "#0B1016"  # darker "screen" for terminal windows

TEXT_PRIMARY = "#EAEDF0"         # off-white, main text
TEXT_SECONDARY = "#9AA5B1"       # muted gray, captions/labels

ACCENT = "#6FA8A0"               # muted teal (primary accent)
ACCENT_BRIGHT = "#8FC4BC"        # brighter teal for emphasis
ACCENT_DIM = "#3D4F4C"           # dim teal for subtle lines/dividers

PANEL_FILL = ACCENT              # kept for backward compatibility
PANEL_FILL_OPACITY = 0.08
PANEL_STROKE_OPACITY = 0.9
PANEL_STROKE_WIDTH = 1.5

COLOR_SAFE = "#7FB299"
COLOR_WARNING = "#D9B36C"
COLOR_DANGER = "#C97B7B"

# One lookup for status colors — reuse anywhere (threat levels, badges…)
SEMANTIC_COLORS = {
    "info": ACCENT,
    "safe": COLOR_SAFE,
    "warning": COLOR_WARNING,
    "danger": COLOR_DANGER,
    "neutral": TEXT_SECONDARY,
}


# ============================================================
# 2 · TYPOGRAPHY
# ============================================================

TITLE_SIZE = 52
HEADING_SIZE = 40
LARGE_TEXT_SIZE = 32
MEDIUM_TEXT_SIZE = 26
SMALL_TEXT_SIZE = 20
CODE_SIZE = 22

# NOTE: missing fonts fall back silently. Check names: `manim --list_fonts`
FONT_MAIN = "Helvetica"
FONT_CODE = "Courier New"


def _text(text, size, color, font=FONT_MAIN, weight=NORMAL):
    """Single factory behind every text helper — styling stays consistent."""
    return Text(text, font_size=size, font=font, color=color, weight=weight)


def Title(text, color=TEXT_PRIMARY):
    return _text(text, TITLE_SIZE, color, weight=BOLD)

def Heading(text, color=TEXT_PRIMARY):
    return _text(text, HEADING_SIZE, color, weight=BOLD)

def LargeText(text, color=TEXT_PRIMARY):
    return _text(text, LARGE_TEXT_SIZE, color)

def MediumText(text, color=TEXT_PRIMARY):
    return _text(text, MEDIUM_TEXT_SIZE, color)

def SmallText(text, color=TEXT_SECONDARY):
    return _text(text, SMALL_TEXT_SIZE, color)

def CodeText(text, color=ACCENT_BRIGHT):
    return _text(text, CODE_SIZE, color, font=FONT_CODE)


# ============================================================
# 3 · PANELS & BOXES
# ============================================================

CORNER_RADIUS = 0.15

SMALL_BOX_WIDTH, SMALL_BOX_HEIGHT = 2.0, 0.8
MEDIUM_BOX_WIDTH, MEDIUM_BOX_HEIGHT = 3.0, 1.4
LARGE_BOX_WIDTH, LARGE_BOX_HEIGHT = 4.0, 2.0

_BOX_SIZES = {
    "small": (SMALL_BOX_WIDTH, SMALL_BOX_HEIGHT),
    "medium": (MEDIUM_BOX_WIDTH, MEDIUM_BOX_HEIGHT),
    "large": (LARGE_BOX_WIDTH, LARGE_BOX_HEIGHT),
}
_TEXT_HELPERS = {"small": SmallText, "medium": MediumText, "large": LargeText}


def Panel(width, height, stroke_color=ACCENT, fill_color=None,
          fill_opacity=PANEL_FILL_OPACITY, stroke_width=PANEL_STROKE_WIDTH,
          stroke_opacity=PANEL_STROKE_OPACITY, corner_radius=CORNER_RADIUS):
    """Generic rounded panel — thin border + low-opacity fill.
    fill_color defaults to the stroke color, so Panel(4, 2, COLOR_DANGER)
    gives you a red-tinted panel automatically."""
    return RoundedRectangle(
        width=width, height=height, corner_radius=corner_radius,
        stroke_color=stroke_color, stroke_width=stroke_width,
        stroke_opacity=stroke_opacity,
        fill_color=fill_color or stroke_color, fill_opacity=fill_opacity,
    )


def SmallBox(stroke_color=ACCENT, fill_color=PANEL_FILL):
    return Panel(SMALL_BOX_WIDTH, SMALL_BOX_HEIGHT, stroke_color, fill_color)

def MediumBox(stroke_color=ACCENT, fill_color=PANEL_FILL):
    return Panel(MEDIUM_BOX_WIDTH, MEDIUM_BOX_HEIGHT, stroke_color, fill_color)

def LargeBox(stroke_color=ACCENT, fill_color=PANEL_FILL):
    return Panel(LARGE_BOX_WIDTH, LARGE_BOX_HEIGHT, stroke_color, fill_color)


def LabeledBox(text, box_size="medium", text_size="small",
               stroke_color=ACCENT, fill_color=PANEL_FILL,
               text_color=TEXT_PRIMARY, width=None, height=None, fit=0.85):
    """Box with a centered, auto-fitted label.
    Pass width/height to override box_size entirely."""
    w, h = _BOX_SIZES[box_size]
    w = width or w
    h = height or h
    box = Panel(w, h, stroke_color=stroke_color, fill_color=fill_color)
    label = _TEXT_HELPERS[text_size](text, color=text_color)
    if label.width > box.width * fit:
        label.scale_to_fit_width(box.width * fit)
    label.move_to(box)
    return VGroup(box, label)


# ============================================================
# 4 · BADGES (status pills)
# ============================================================

def Badge(text, kind="info", font_size=SMALL_TEXT_SIZE * 0.9):
    """Status pill: Badge("ENCRYPTED", kind="safe").
    kind: info | safe | warning | danger | neutral (see SEMANTIC_COLORS)."""
    color = SEMANTIC_COLORS.get(kind, ACCENT)
    label = _text(text, font_size, color, weight=BOLD)
    h = label.height + 0.32
    pill = RoundedRectangle(
        width=label.width + 0.55, height=h, corner_radius=h / 2,
        stroke_color=color, stroke_width=1.5,
        fill_color=color, fill_opacity=0.12,
    )
    label.move_to(pill)
    return VGroup(pill, label)


# ============================================================
# 5 · DIAGRAM PARTS
# ============================================================

def Connector(start, end, label=None, color=ACCENT, label_color=TEXT_SECONDARY,
              stroke_width=3, buff=0.2, side=UP, label_buff=0.15, dashed=False):
    """Labeled arrow between two points or mobjects.
    side: where the label sits (UP/DOWN/LEFT/RIGHT). dashed=True for
    'possible/indirect' flows. NOTE: mobjects connect center-to-center —
    for edges use Connector(a.get_right(), b.get_left())."""
    arrow = Arrow(
        start=start, end=end, color=color, stroke_width=stroke_width,
        buff=buff, max_tip_length_to_length_ratio=0.15,
    )
    if dashed:
        arrow = DashedVMobject(arrow, num_dashes=12, dashed_ratio=0.6)
    if label is None:
        return VGroup(arrow)
    label_text = SmallText(label, color=label_color)
    label_text.next_to(arrow, side, buff=label_buff)
    return VGroup(arrow, label_text)


PACKET_WIDTH = 1.4
PACKET_HEIGHT = 0.6


def Packet(text, color=ACCENT, fill_color=None, text_color=None):
    """Small pill meant to travel along a path (SYN, ACK, credentials…)."""
    fill = fill_color or color
    txt_color = text_color or TEXT_PRIMARY
    body = RoundedRectangle(
        width=PACKET_WIDTH, height=PACKET_HEIGHT,
        corner_radius=PACKET_HEIGHT / 2,
        stroke_color=color, stroke_width=PANEL_STROKE_WIDTH,
        fill_color=fill, fill_opacity=0.2,
    )
    label = CodeText(text, color=txt_color).scale(0.7)
    if label.width > body.width * 0.85:
        label.scale_to_fit_width(body.width * 0.85)
    label.move_to(body)
    return VGroup(body, label)


# ============================================================
# 6 · ICONS (line-style, match the theme)
# ============================================================

def LaptopIcon(color=ACCENT, stroke_width=2.5):
    screen = RoundedRectangle(width=1.5, height=1.0, corner_radius=0.08)
    base = RoundedRectangle(width=2.0, height=0.14, corner_radius=0.07)
    base.next_to(screen, DOWN, buff=0.08)
    return VGroup(screen, base).set_stroke(color, width=stroke_width).set_fill(opacity=0)


def ServerIcon(color=ACCENT, stroke_width=2.5):
    rack = RoundedRectangle(width=1.0, height=1.5, corner_radius=0.1)
    units = VGroup(*[
        RoundedRectangle(width=0.7, height=0.26, corner_radius=0.05)
        for _ in range(3)
    ]).arrange(DOWN, buff=0.14)
    units.move_to(rack)
    leds = VGroup(*[
        Dot(radius=0.045, color=COLOR_SAFE).move_to(u.get_left() + RIGHT * 0.15)
        for u in units
    ])
    rack.set_stroke(color, width=stroke_width).set_fill(opacity=0)
    units.set_stroke(color, width=stroke_width * 0.7).set_fill(opacity=0)
    return VGroup(rack, units, leds)


def PhoneIcon(color=ACCENT, stroke_width=2.5):
    body = RoundedRectangle(width=0.8, height=1.4, corner_radius=0.14)
    screen = RoundedRectangle(width=0.62, height=1.05, corner_radius=0.05)
    screen.move_to(body.get_center() + UP * 0.08)
    speaker = Line(LEFT, RIGHT, color=color, stroke_width=stroke_width * 0.8)
    speaker.set_width(0.2).move_to(body.get_top() + DOWN * 0.12)
    home = Dot(radius=0.05, color=color).move_to(body.get_bottom() + UP * 0.13)
    frame = VGroup(body, screen, speaker)
    frame.set_stroke(color, width=stroke_width).set_fill(opacity=0)
    return VGroup(frame, home)


def LockIcon(color=ACCENT, stroke_width=2.5):
    body = RoundedRectangle(width=0.75, height=0.6, corner_radius=0.1)
    body.set_stroke(color, width=stroke_width).set_fill(color, opacity=0.15)
    shackle = Arc(radius=0.24, start_angle=0, angle=PI,
                  color=color, stroke_width=stroke_width)
    shackle.move_arc_center_to(body.get_top() + DOWN * 0.02)
    keyhole = VGroup(
        Dot(radius=0.06, color=color),
        Line(ORIGIN, DOWN * 0.14, color=color, stroke_width=stroke_width * 0.8),
    ).arrange(DOWN, buff=0.02).move_to(body)
    return VGroup(shackle, body, keyhole)


def ShieldIcon(color=ACCENT, stroke_width=2.5, checked=False):
    w, h = 0.9, 1.05
    shield = Polygon(
        [-w / 2, h * 0.5, 0], [w / 2, h * 0.5, 0],
        [w / 2, -h * 0.1, 0], [0, -h * 0.5, 0],
        [-w / 2, -h * 0.1, 0],
    )
    shield.round_corners(0.1)
    shield.set_stroke(color, width=stroke_width).set_fill(color, opacity=0.12)
    if not checked:
        return shield
    mark = VGroup(
        Line([-0.13, -0.02, 0], [-0.03, -0.14, 0]),
        Line([-0.03, -0.14, 0], [0.17, 0.1, 0]),
    ).set_stroke(color, width=stroke_width).move_to(shield.get_center() + UP * 0.03)
    return VGroup(shield, mark)


def FirewallIcon(width=2.4, height=1.1, color=ACCENT, stroke_width=2.5,
                 rows=3, cols=3):
    """Brick-wall rectangle — pair with a danger-colored label or packet flow."""
    wall = RoundedRectangle(width=width, height=height, corner_radius=0.06)
    parts = [wall]
    row_h = height / rows
    for i in range(1, rows):  # horizontal brick lines
        y = height / 2 - i * row_h
        parts.append(Line([-width / 2, y, 0], [width / 2, y, 0]))
    for i in range(rows):  # staggered vertical joints
        y_top = height / 2 - i * row_h
        stagger = (width / cols) / 2 if i % 2 else 0
        for j in range(cols):
            x = -width / 2 + j * (width / cols) + stagger
            if -width / 2 < x < width / 2:
                parts.append(Line([x, y_top - row_h, 0], [x, y_top, 0]))
    icon = VGroup(*parts)
    icon.set_stroke(color, width=stroke_width).set_fill(opacity=0)
    return icon

# ============================================================
# 7. DIAGRAM KIT — nodes, links, graphs, failure marks
# ============================================================

def _to_3d(p):
    """Normalize a point (list/tuple/np) to a 3D np array."""
    p = np.array(p, dtype=float)
    return np.array([p[0], p[1], 0.0]) if p.shape == (2,) else p


def NetNode(label=None, radius=0.42, color=ACCENT, fill_opacity=0.15,
            label_color=TEXT_PRIMARY, font_size=None):
    """Circular network-diagram node with a short label inside (A, B, SW…)."""
    circle = Circle(radius=radius, stroke_color=color, stroke_width=2.5,
                    fill_color=color, fill_opacity=fill_opacity)
    if label is None:
        return circle
    text = Text(str(label), font=FONT_MAIN, weight=BOLD,
                font_size=font_size or SMALL_TEXT_SIZE * 0.9, color=label_color)
    if text.width > circle.width * 0.7:
        text.scale_to_fit_width(circle.width * 0.7)
    text.move_to(circle)
    return VGroup(circle, text)


def Link(start, end, color=ACCENT_DIM, stroke_width=2.5, label=None,
         label_color=TEXT_SECONDARY, label_buff=0.12, trim=0.0):
    """Plain undirected connection (no arrowhead — use Connector for arrows).
    start/end: points or mobjects (mobjects connect center-to-center;
    pair with edge_toward to hit an edge instead). trim pulls each end
    back along the line — e.g. trim=0.42 to stop at node edges.
    Returns a Line, or VGroup(line, label) when a label is given."""
    p1 = _to_3d(start.get_center() if isinstance(start, Mobject) else start)
    p2 = _to_3d(end.get_center() if isinstance(end, Mobject) else end)
    if trim and np.linalg.norm(p2 - p1) > 2 * trim:
        u = (p2 - p1) / np.linalg.norm(p2 - p1)
        p1, p2 = p1 + u * trim, p2 - u * trim
    line = Line(p1, p2, color=color, stroke_width=stroke_width)
    if label is None:
        return line
    tag = SmallText(label, color=label_color)
    tag.next_to(line, UP, buff=label_buff)
    return VGroup(line, tag)


def edge_toward(mobj, target):
    """Point on mobj's bounding-box edge in the direction of target.
    Use it to attach links/arrows to the EDGE of oddly-shaped mobjects
    (icons) instead of poking through their center."""
    c = mobj.get_center()
    d = _to_3d(target) - c
    if np.linalg.norm(d) < 1e-9:
        return c
    half = np.array([mobj.width / 2, mobj.height / 2, 0])
    ratios = [half[i] / abs(d[i]) if abs(d[i]) > 1e-9 else np.inf for i in (0, 1)]
    return c + d * min(ratios)


def circular_layout(names, radius=1.5, center=ORIGIN, start_angle=PI / 2):
    """Evenly place names around a circle → {name: point} for GraphDiagram.
    Accepts a string ('ABCDE') or any iterable of names."""
    names = list(names)
    n = len(names)
    c = _to_3d(center)
    return {
        name: c + radius * np.array(
            [np.cos(start_angle + i * TAU / n),
             np.sin(start_angle + i * TAU / n), 0])
        for i, name in enumerate(names)
    }


class GraphDiagram(VGroup):
    """Whole node-link diagram from a spec:

        pos = circular_layout("ABCDE", radius=1.3, center=DOWN * 0.4)
        net = GraphDiagram(pos, [("A", "B"), ("B", "C"), ("E", "A")])

    Access pieces by name for animating: net.nodes["A"], net.links[("A", "B")].
    Edges may carry a label: ("A", "B", "10 Gbps").
    """

    def __init__(self, positions, edges=(), node_color=ACCENT,
                 link_color=ACCENT_DIM, node_radius=0.42, trim=None,
                 node_kwargs=None, link_kwargs=None):
        self.nodes = {}
        self.links = {}
        trim = node_radius if trim is None else trim
        node_kwargs, link_kwargs = node_kwargs or {}, link_kwargs or {}

        for name, point in positions.items():
            node = NetNode(str(name), radius=node_radius,
                           color=node_color, **node_kwargs)
            node.move_to(_to_3d(point))
            self.nodes[name] = node

        link_mobs = []
        for edge in edges:
            a, b, *rest = edge
            label = rest[0] if rest else None
            link = Link(self.nodes[a], self.nodes[b], color=link_color,
                        label=label, trim=trim, **link_kwargs)
            self.links[(a, b)] = self.links[(b, a)] = link
            link_mobs.append(link)

        super().__init__(*link_mobs, *self.nodes.values())


def FailMark(target, size=None, color=COLOR_DANGER, stroke_width=4):
    """Red ✕ overlaid on a mobject or point — 'this node/link is down'.
    size defaults to ~90% of the target's width; pass size explicitly for
    long thin targets (e.g. FailMark(link.get_center(), size=0.4))."""
    if isinstance(target, Mobject):
        center, size = target.get_center(), size or target.width * 0.9
    else:
        center, size = _to_3d(target), size or 0.6
    s = size / 2
    mark = VGroup(
        Line([-s, -s, 0], [s, s, 0]),
        Line([-s, s, 0], [s, -s, 0]),
    ).set_stroke(color, width=stroke_width)
    mark.move_to(center)
    return mark

# ============================================================
# 8 · TERMINAL WINDOW
# ============================================================

class Terminal(VGroup):
    """Dark terminal window: title bar, divider, monospace lines.

    Pass lines as plain strings, or (text, color) tuples for colored output.
    Give a fixed ``height`` to reserve room for lines added later.

        term = Terminal([("$ nmap -sV 10.0.0.5", ACCENT_BRIGHT)], height=3.4)
        self.play(FadeIn(term, shift=0.2 * UP))
        self.play(TypeIn(term.lines[0]))
        self.play(TypeIn(term.add_line("22/tcp  open  ssh")))
    """

    def __init__(self, lines: Sequence[Union[str, Tuple[str, str]]] = (),
                 title: str = "user@host: ~", width: float = 9.0,
                 height: Optional[float] = None, font_size: float = CODE_SIZE,
                 line_buff: float = 0.16,
                 background: str = TERMINAL_BACKGROUND):
        pad, gap = 0.32, 0.2
        self._font_size = font_size
        self._line_buff = line_buff
        self._pad = pad
        self._gap = gap
        self._width = width
        self._fixed_height = height is not None

        line_mobs = VGroup(*[self._make_line(ln) for ln in lines])
        line_mobs.arrange(DOWN, aligned_edge=LEFT, buff=line_buff)
        self._fit_lines(line_mobs)

        title_text = Text(title, font=FONT_CODE, font_size=SMALL_TEXT_SIZE,
                          color=TEXT_SECONDARY)
        dots = VGroup(*[
            Dot(radius=0.05, color=c, fill_opacity=0.9)
            for c in (COLOR_DANGER, COLOR_WARNING, COLOR_SAFE)
        ]).arrange(RIGHT, buff=0.14)

        body_h = (2 * pad + max(title_text.height, dots.height)
                  + 2 * gap + line_mobs.height)
        if height:
            body_h = max(body_h, height)
        body = RoundedRectangle(
            width=width, height=max(body_h, 1.3), corner_radius=0.14,
            fill_color=background, fill_opacity=1,
            stroke_color=ACCENT_DIM, stroke_width=PANEL_STROKE_WIDTH,
        )

        title_text.next_to(body.get_corner(UL), DR, buff=pad)
        dots.next_to(body.get_corner(UR), DL, buff=pad)
        divider = Line(LEFT, RIGHT, color=ACCENT_DIM, stroke_width=1)
        divider.set_width(width - 2 * pad)
        divider.next_to(VGroup(title_text, dots), DOWN, buff=gap)

        if len(line_mobs):
            line_mobs.next_to(divider, DOWN, buff=gap)
            line_mobs.align_to(title_text, LEFT)

        super().__init__(body, title_text, dots, divider, line_mobs)
        self.body = body
        self.title_text = title_text
        self.dots = dots
        self.divider = divider
        self.lines = line_mobs

    def _make_line(self, line):
        text, color = line if isinstance(line, tuple) else (line, TEXT_PRIMARY)
        return Text(text, font=FONT_CODE, font_size=self._font_size, color=color)

    def _fit_lines(self, line_mobs):
        max_w = self._width - 2 * self._pad
        for ln in line_mobs:
            if ln.width > max_w:
                ln.scale_to_fit_width(max_w)

    def add_line(self, line):
        """Append a line below the last one. Window grows unless a fixed
        ``height`` was given. Returns the new line so it can be animated."""
        new = self._make_line(line)
        if len(self.lines):
            new.next_to(self.lines[-1], DOWN, buff=self._line_buff)
            new.align_to(self.lines, LEFT)
        else:
            new.next_to(self.divider, DOWN, buff=self._gap)
            new.align_to(self.title_text, LEFT)
        self._fit_lines(VGroup(new))
        if not self._fixed_height:
            top = self.body.get_top()
            self.body.stretch_to_fit_height(self.body.height + new.height + self._line_buff)
            self.body.move_to(top, aligned_edge=UP)
        self.lines.add(new)
        #self.add(new)
        return new


# ============================================================
# 9 · COMPOSITION (section openers, lists, cards, captions)
# ============================================================

def Divider(width=4.5):
    """Hairline with a short bright segment — editorial rule."""
    base = Line(LEFT, RIGHT, color=ACCENT_DIM, stroke_width=2).set_width(width)
    tip = Line(LEFT, RIGHT, color=ACCENT, stroke_width=4).set_width(width * 0.18)
    tip.align_to(base, LEFT)
    return VGroup(base, tip)


def SectionHeader(title, kicker=None, subtitle=None):
    """Section opener: small teal kicker, big title, accent rule, optional
    subtitle. Left-aligned — pin with .to_corner(UL) or .to_edge(UP)."""
    parts = []
    if kicker:
        parts.append(_text(kicker.upper(), SMALL_TEXT_SIZE * 0.85, ACCENT_BRIGHT, weight=BOLD))
    parts.append(Title(title))
    head = VGroup(*parts).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    rule = Divider(width=max(3.0, head.width * 0.8))
    rule.next_to(head, DOWN, buff=0.18)
    items = [head, rule]
    if subtitle:
        sub = SmallText(subtitle)
        sub.next_to(rule, DOWN, buff=0.25)
        items.append(sub)
    return VGroup(*items)


def InfoCard(title, body, width=6.0, title_color=ACCENT_BRIGHT):
    """Definition panel: bold accent title + secondary body text."""
    pad = 0.35
    inner_w = width - 2 * pad
    title_m = _text(title, MEDIUM_TEXT_SIZE, title_color, weight=BOLD)
    body_m = _text(body, SMALL_TEXT_SIZE, TEXT_SECONDARY)
    if body_m.width > inner_w:
        body_m.scale_to_fit_width(inner_w)
    if title_m.width > inner_w:
        title_m.scale_to_fit_width(inner_w)
    content = VGroup(title_m, body_m).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    panel = Panel(width, content.height + 2 * pad)
    content.move_to(panel)
    content.align_to(panel.get_left() + RIGHT * pad, LEFT)
    return VGroup(panel, content)


def BulletList(*items, buff=0.3, marker="dot", color=TEXT_PRIMARY,
               marker_color=ACCENT, font_size=MEDIUM_TEXT_SIZE):
    """Styled bullet list. marker: 'dot' | 'square' | 'number'."""
    rows = []
    for i, item in enumerate(items, start=1):
        text = _text(item, font_size, color)
        if marker == "dot":
            m = Dot(radius=0.06, color=marker_color)
        elif marker == "square":
            m = Square(side_length=0.12).set_fill(marker_color, 1).set_stroke(width=0).rotate(PI / 4)
        else:  # numbered circle
            circle = Circle(radius=0.24, stroke_color=marker_color, stroke_width=1.8)
            circle.set_fill(marker_color, opacity=0.1)
            num = _text(str(i), font_size * 0.55, marker_color, weight=BOLD).move_to(circle)
            m = VGroup(circle, num)
        m.next_to(text, LEFT, buff=0.3)
        rows.append(VGroup(m, text))
    return VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=buff)


def Caption(text, buff=0.4):
    """Secondary-colored caption pinned to the bottom of the frame."""
    return SmallText(text).to_edge(DOWN, buff=buff)


# ============================================================
# 10 · SCENE BASE & ANIMATION HELPERS
# ============================================================

def apply_theme(scene):
    """Set the standard dark background on a scene.
    Tip: to fix it project-wide, put `background_color = #12181F`
    in a manim.cfg instead — then even this call is optional."""
    scene.camera.background_color = BACKGROUND_COLOR


class CyberScene(Scene):
    """Inherit from this instead of Scene and the theme applies itself:

        class MyScene(CyberScene):
            def construct(self): ...
    """

    def setup(self):
        apply_theme(self)


def TypeIn(text_mobj, lag_ratio=0.08, shift=0.06):
    """Typewriter reveal for any Text-based mobject (incl. CodeText).
    Use with Terminal lines: self.play(TypeIn(term.lines[0]), run_time=1.5)"""
    glyphs = text_mobj.family_members_with_points()
    return LaggedStart(
        *[FadeIn(g, shift=shift * UP) for g in glyphs],
        lag_ratio=lag_ratio,
    )

 # ============================================================
# SIGNAL KIT — waveforms, scopes, bit encodings
# for physical-layer scenes (encoding, modulation, noise…)
# ============================================================

def WaveCurve(fn, x_range=(0.0, 1.0), width=8.0, amplitude=0.75,
              color=ACCENT_BRIGHT, stroke_width=3, samples=800):
    """Plot y = fn(x) as a curve in scene units.
    fn should be continuous (jumps become near-vertical lines); for
    piecewise-constant signals use LevelWave/BitWave instead.
    The curve spans `width` scene units; y = 1 maps to `amplitude`."""
    x0, x1 = x_range
    ts = np.linspace(x0, x1, samples)
    pts = [np.array([(t - x0) / (x1 - x0) * width, amplitude * fn(t), 0.0])
           for t in ts]
    curve = VMobject(stroke_color=color, stroke_width=stroke_width,
                     fill_opacity=0)
    curve.set_points_as_corners(pts)
    return curve


def SineWave(width=8.0, cycles=3.0, amplitude=0.75, phase=0.0,
             color=ACCENT_BRIGHT, stroke_width=3):
    """Pure sine wave: `cycles` periods across `width` scene units."""
    return WaveCurve(lambda t: np.sin(TAU * cycles * t + phase),
                     width=width, amplitude=amplitude, color=color,
                     stroke_width=stroke_width,
                     samples=max(800, 40 * int(cycles)))


def LevelWave(levels, width=8.0, amplitude=0.75, color=ACCENT_BRIGHT,
              stroke_width=3):
    """Piecewise-constant waveform — one level per equal-width symbol
    slot. Levels are y-values (±1 → ±amplitude on screen). Crisp vertical
    edges: the right tool for NRZ / multilevel / PAM signals."""
    n = len(levels)
    cell = width / n

    def pt(x, y):
        return np.array([x, amplitude * y, 0.0])

    pts = [pt(0.0, levels[0])]
    for i in range(1, n):
        x = i * cell
        pts.append(pt(x, levels[i - 1]))
        pts.append(pt(x, levels[i]))
    pts.append(pt(width, levels[-1]))
    curve = VMobject(stroke_color=color, stroke_width=stroke_width,
                     fill_opacity=0)
    curve.set_points_as_corners(pts)
    return curve


def BitWave(bits, width=8.0, amplitude=0.75, high=1.0, low=-1.0,
            color=ACCENT_BRIGHT, stroke_width=3):
    """NRZ encoding of a bit string ('1011…'): 1 → high, 0 → low."""
    levels = [high if b == "1" else low for b in str(bits)]
    return LevelWave(levels, width=width, amplitude=amplitude,
                     color=color, stroke_width=stroke_width)


def BitRow(bits, cell=1.0, color=TEXT_SECONDARY):
    """Monospace bit characters, one centered per slot of width `cell`.
    Pair with BitWave (same width/n cell) and center both on the same
    point so each digit sits above its wave segment."""
    chars = VGroup()
    for i, b in enumerate(str(bits)):
        c = CodeText(b, color=color)
        c.move_to(np.array([(i + 0.5) * cell, 0.0, 0.0]))
        chars.add(c)
    return chars


def Scope(width=10.0, height=2.8, title=None, cells=(12, 4),
          background=TERMINAL_BACKGROUND):
    """Oscilloscope panel: dark screen, faint grid, brighter center line.
    Place waves with wave.move_to(scope.body.get_center()).
    title: optional small tab straddling the top-left border."""
    body = RoundedRectangle(width=width, height=height, corner_radius=0.12,
                            fill_color=background, fill_opacity=1,
                            stroke_color=ACCENT_DIM,
                            stroke_width=PANEL_STROKE_WIDTH)
    cols, rows = cells
    grid = VGroup()
    for i in range(1, cols):
        x = body.get_left()[0] + i * width / cols
        grid.add(Line([x, body.get_bottom()[1] + 0.1, 0],
                      [x, body.get_top()[1] - 0.1, 0],
                      color=ACCENT_DIM, stroke_width=1, stroke_opacity=0.35))
    for j in range(1, rows):
        y = body.get_bottom()[1] + j * height / rows
        grid.add(Line([body.get_left()[0] + 0.1, y, 0],
                      [body.get_right()[0] - 0.1, y, 0],
                      color=ACCENT_DIM, stroke_width=1, stroke_opacity=0.35))
    mid = Line([body.get_left()[0] + 0.1, body.get_center()[1], 0],
               [body.get_right()[0] - 0.1, body.get_center()[1], 0],
               color=ACCENT_DIM, stroke_width=1.5, stroke_opacity=0.6)
    scope = VGroup(body, grid, mid)
    if title:
        tab = SmallText(title, color=TEXT_SECONDARY).scale(0.7)
        tab.next_to(body, UP, buff=-0.16).align_to(body, LEFT)
        scope.add(tab)
    scope.body = body          # anchor for placing waves
    scope.center_line = mid
    return scope
