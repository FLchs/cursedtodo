from collections.abc import Callable
from curses import A_BOLD, curs_set, window

from cursedtodo.utils.textpad import Textbox


class Field:
    def __init__(
        self,
        y: int,
        window: window,
        name: str,
        id: str,
        validator: Callable[[int], int],
    ):
        self.window = window
        self.name = name
        self.id = id
        self.y = y
        self.textwindow = window.derwin(1, 50, y, 15)
        self.textbox = Textbox(self.textwindow, insert_mode=True) # type: ignore
        self.value = ""
        self.validator = validator
        self.render()

    def render(self) -> None:
        self.window.addstr(self.y, 1, f"{self.name}: ", A_BOLD)
        self.textwindow.move(0, 0)
        self.textwindow.addstr(self.value)
        self.textwindow.move(0, max(len(self.value) - 1, 0))
        self.textwindow.refresh()

    def save(self) -> None:
        self.value = self.textbox.gather() # type: ignore

    def focus(self) -> None:
        curs_set(1)
        self.textwindow.move(0, max(len(self.value) - 1, 0))
        self.textbox.edit(self.validator) # type: ignore
        self.value = self.textbox.gather() # type: ignore
