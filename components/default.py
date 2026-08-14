from manim import *

TITLE_SIZE = 52
HEADING_SIZE = 40
LARGE_TEXT_SIZE = 32
MEDIUM_TEXT_SIZE = 26
SMALL_TEXT_SIZE = 20
CODE_SIZE = 22

def Title(text):
    return Text(text, font_size=TITLE_SIZE)

def Heading(text):
    return Text(text, font_size=HEADING_SIZE)

def LargeText(text):
    return Text(text, font_size=LARGE_TEXT_SIZE)

def MediumText(text):
    return Text(text, font_size=MEDIUM_TEXT_SIZE)

def SmallText(text):
    return Text(text, font_size=SMALL_TEXT_SIZE)

SMALL_BOX_WIDTH = 2.0
SMALL_BOX_HEIGHT = 0.8

MEDIUM_BOX_WIDTH = 3.0
MEDIUM_BOX_HEIGHT = 1.4

LARGE_BOX_WIDTH = 4.0
LARGE_BOX_HEIGHT = 2.0

def SmallBox():
    return RoundedRectangle(
        width=SMALL_BOX_WIDTH,
        height=SMALL_BOX_HEIGHT,
        corner_radius=0.15,
    )

def MediumBox():
    return RoundedRectangle(
        width=MEDIUM_BOX_WIDTH,
        height=MEDIUM_BOX_HEIGHT,
        corner_radius=0.15,
    )

def LargeBox():
    return RoundedRectangle(
        width=LARGE_BOX_WIDTH,
        height=LARGE_BOX_HEIGHT,
        corner_radius=0.15,
    )
