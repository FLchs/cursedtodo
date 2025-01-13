from dataclasses import dataclass
import os
from typing import Optional

from cursedtodo.utils.colors import WHITE, get_color


@dataclass
class Calendar:
    id: int
    name: str
    path: str
    color: Optional[str] = "white"
    default: Optional[bool] = None
    color_attr: int = 0

    def __post_init__(self) -> None:
        self.color_attr = get_color(self.color)
        self.path = os.path.expanduser(self.path)
