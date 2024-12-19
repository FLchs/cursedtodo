from curses import (
    COLOR_BLACK,
    COLOR_BLUE,
    COLOR_CYAN,
    COLOR_GREEN,
    COLOR_MAGENTA,
    COLOR_RED,
    COLOR_WHITE,
    COLOR_YELLOW,
    color_pair,
    init_pair,
)
from dataclasses import dataclass
import os
from typing import Optional

COLOR_MAP = {
    "black": COLOR_BLACK,
    "red": COLOR_RED,
    "green": COLOR_GREEN,
    "yellow": COLOR_YELLOW,
    "blue": COLOR_BLUE,
    "magenta": COLOR_MAGENTA,
    "cyan": COLOR_CYAN,
    "white": COLOR_WHITE,
}


@dataclass
class Calendar:
    id: int
    name: str
    path: str
    color: Optional[str] = "white"
    default: Optional[bool] = None
    color_attr: int = 0

    def init_color(self) -> None:
        if self.color_attr == 0:
            # Determine the actual color value (default to black if None or invalid string)
            if self.color is None:
                color_value = COLOR_WHITE
            else:
                color_value = COLOR_MAP.get(self.color.lower(), COLOR_WHITE)

            init_pair(self.id + 130, color_value, -1)
            self.color_attr = color_pair(self.id + 130)

    def __post_init__(self) -> None:
        self.path = os.path.expanduser(self.path)
