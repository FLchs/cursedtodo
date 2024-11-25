from collections.abc import Callable
from curses import A_BOLD, COLOR_WHITE, KEY_RESIZE, color_pair, init_pair, window
import curses

from cursedtodo.utils.textinput import TextInput
from cursedtodo.views.form.base_field import BaseField


class CategoriesField(BaseField):
    def __init__(
        self,
        y: int,
        window: window,
        id: str,
        validator: Callable[[int | str], int | str],
    ):
        super().__init__(y, window, id, id, validator)
        self.value: list[str] = []
        self.textwindow = window.derwin(1, 20, y, 15)
        init_pair(45, COLOR_WHITE, curses.COLOR_BLACK)
        self.textwindow.bkgd(' ', color_pair(45))
        self.validator = validator
        self.editor = TextInput(self.textwindow, "", self._validator)

    def _validator(self, ch: str | int) -> str | int:
        if ch == KEY_RESIZE:
            self.value = self.editor.gather().split(",")
        return ch

    def render(self) -> None:
        self.window.addstr(self.y, 1, f"{self.id.capitalize()}: ", A_BOLD)
        self.textwindow.move(0, 0)
        value = ", ".join(self.value) 
        self.editor.set_value(value)
        self.editor.render()

    def focus(self) -> None:
        self.editor.main()
        self.value = self.editor.gather().split(",")