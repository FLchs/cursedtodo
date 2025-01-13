from curses import (
    COLOR_WHITE,
    COLOR_BLUE,
    COLOR_CYAN,
    COLOR_GREEN,
    COLOR_MAGENTA,
    COLOR_RED,
    COLOR_YELLOW,
    color_pair,
    init_pair,
)

init_pair(11, COLOR_WHITE, -1)
init_pair(12, COLOR_BLUE, -1)
init_pair(13, COLOR_CYAN, -1)
init_pair(14, COLOR_GREEN, -1)
init_pair(15, COLOR_YELLOW, -1)
init_pair(16, COLOR_MAGENTA, -1)
init_pair(17, COLOR_RED, -1)


WHITE = color_pair(11)
BLUE = color_pair(12)
CYAN = color_pair(13)
GREEN = color_pair(14)
YELLOW = color_pair(15)
MAGENTA = color_pair(16)
RED = color_pair(17)

COLORS = [BLUE, CYAN, GREEN, YELLOW, MAGENTA, RED]


def get_color(name: str | None) -> int:
    if name is None:
        return WHITE
    name = name.upper()
    if name == "WHITE":
        return WHITE
    elif name == "BLUE":
        return BLUE
    elif name == "CYAN":
        return CYAN
    elif name == "GREEN":
        return GREEN
    elif name == "YELLOW":
        return YELLOW
    elif name == "MAGENTA":
        return MAGENTA
    elif name == "RED":
        return RED
    else:
        return WHITE


def random_color(string: str) -> int:
    hashed_value = hash(string)
    index = hashed_value % len(COLORS)
    return COLORS[index]
