from manim import *

# ============================================================
# COLOR PALETTE
# Dark editorial style: deep slate background, muted teal accent,
# off-white text. Inspired by clean data-journalism report style,
# adapted for a dark theme.
# ============================================================

BACKGROUND_COLOR = "#12181F"      # deep slate / near-black navy
PANEL_BACKGROUND = "#1B242E"      # slightly lighter panel background

TEXT_PRIMARY = "#EAEDF0"          # off-white, main text
TEXT_SECONDARY = "#9AA5B1"        # muted gray, captions/labels

ACCENT = "#6FA8A0"                # muted teal/steel blue (primary accent)
ACCENT_BRIGHT = "#8FC4BC"         # brighter teal for highlights/emphasis
ACCENT_DIM = "#3D4F4C"            # dim teal, for subtle lines/dividers

PANEL_FILL = "#6FA8A0"            # teal fill for panels (used at low opacity)
PANEL_FILL_OPACITY = 0.08
PANEL_STROKE_OPACITY = 0.9
PANEL_STROKE_WIDTH = 1.5

# Semantic colors (kept muted/desaturated to match the editorial feel)
COLOR_SAFE = "#7FB299"
COLOR_WARNING = "#D9B36C"
COLOR_DANGER = "#C97B7B"


# ============================================================
# TYPOGRAPHY
# ============================================================

TITLE_SIZE = 52
HEADING_SIZE = 40
LARGE_TEXT_SIZE = 32
MEDIUM_TEXT_SIZE = 26
SMALL_TEXT_SIZE = 20
CODE_SIZE = 22

FONT_MAIN = "Helvetica"    # clean sans-serif body/heading font
FONT_CODE = "Courier New"  # monospace for code/terminal elements


def Title(text, color=TEXT_PRIMARY):
    return Text(text, font_size=TITLE_SIZE, font=FONT_MAIN, color=color, weight=BOLD)


def Heading(text, color=TEXT_PRIMARY):
    return Text(text, font_size=HEADING_SIZE, font=FONT_MAIN, color=color, weight=BOLD)


def LargeText(text, color=TEXT_PRIMARY):
    return Text(text, font_size=LARGE_TEXT_SIZE, font=FONT_MAIN, color=color)


def MediumText(text, color=TEXT_PRIMARY):
    return Text(text, font_size=MEDIUM_TEXT_SIZE, font=FONT_MAIN, color=color)


def SmallText(text, color=TEXT_SECONDARY):
    return Text(text, font_size=SMALL_TEXT_SIZE, font=FONT_MAIN, color=color)


def CodeText(text, color=ACCENT_BRIGHT):
    return Text(text, font_size=CODE_SIZE, font=FONT_CODE, color=color)


# ============================================================
# BOXES / PANELS
# Thin teal border, low-opacity teal fill, rounded corners —
# matches the "panel" look of the reference style.
# ============================================================

SMALL_BOX_WIDTH = 2.0
SMALL_BOX_HEIGHT = 0.8
MEDIUM_BOX_WIDTH = 3.0
MEDIUM_BOX_HEIGHT = 1.4
LARGE_BOX_WIDTH = 4.0
LARGE_BOX_HEIGHT = 2.0

CORNER_RADIUS = 0.15


def _panel(width, height, stroke_color, fill_color, corner_radius=CORNER_RADIUS):
    return RoundedRectangle(
        width=width,
        height=height,
        corner_radius=corner_radius,
        stroke_color=stroke_color,
        stroke_width=PANEL_STROKE_WIDTH,
        stroke_opacity=PANEL_STROKE_OPACITY,
        fill_color=fill_color,
        fill_opacity=PANEL_FILL_OPACITY,
    )


def SmallBox(stroke_color=ACCENT, fill_color=PANEL_FILL):
    return _panel(SMALL_BOX_WIDTH, SMALL_BOX_HEIGHT, stroke_color, fill_color)


def MediumBox(stroke_color=ACCENT, fill_color=PANEL_FILL):
    return _panel(MEDIUM_BOX_WIDTH, MEDIUM_BOX_HEIGHT, stroke_color, fill_color)


def LargeBox(stroke_color=ACCENT, fill_color=PANEL_FILL):
    return _panel(LARGE_BOX_WIDTH, LARGE_BOX_HEIGHT, stroke_color, fill_color)


# ============================================================
# SCENE HELPER
# Call this at the start of a scene's construct() to set the
# dark editorial background.
# ============================================================

def apply_theme(scene):
    """Sets the standard background color for a scene."""
    scene.camera.background_color = BACKGROUND_COLOR
