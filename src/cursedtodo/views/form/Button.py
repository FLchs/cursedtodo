from curses import A_NORMAL, A_STANDOUT, curs_set, window
from typing import Callable


class Button:
    def __init__(
        self,
        window: window,
        y: int,
        x: int,
        name: str,
        action: Callable[[], bool],
        validator: Callable[[int | str], int | str],
    ) -> None:
        self.window = window
        self.x = x
        self.y = y
        self.name = name
        self.action = action
        self.validator = validator

    def render(self, y: int, x: int) -> None:
        self.y = y
        self.x = x
        self.window.addstr(y, x, self.name)

    def focus(self) -> bool | None:
        curs_set(0)
        while True:
            self.window.chgat(self.y, self.x, len(self.name), A_STANDOUT)
            k = self.window.getch()
            self.validator(k)
            if k == 10:
                return self.action()
            if k == 9:
                self.window.chgat(self.y, self.x, A_NORMAL)
                self.window.refresh()
                break
        return None
