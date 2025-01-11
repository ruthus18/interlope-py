import typing as t


class Color(t.NamedTuple):
    # values range: 0 - 255
    r: int
    g: int
    b: int
    a: float = 1.0


class GLColor(t.NamedTuple):
    # values range: 0.0 - 1.0
    r: float
    g: float
    b: float
    a: float = 1.0


def color_rgb_to_gl(color: Color) -> GLColor:
    return (color.r / 255, color.g / 255, color.b / 255, color.a)


BLACK = color_rgb_to_gl(
    Color(0, 0, 0)
)
WHITE = color_rgb_to_gl(
    Color(255, 255, 255)
)
DARK = color_rgb_to_gl(
    Color(40, 40, 40)
)
DARK2 = color_rgb_to_gl(
    Color(29, 32, 33)
)
NIGHT_BLUE = color_rgb_to_gl(
    Color(1, 45, 84)
)
LIGHT_YELLOW = color_rgb_to_gl(
    Color(255, 255, 50)
)
