from collections.abc import Callable
from curses import A_BOLD, COLOR_BLACK, COLOR_WHITE, KEY_RESIZE, color_pair, init_pair, window

from cursedtodo.utils.textinput import TextInput
from cursedtodo.views.form.base_field import BaseField


class TextInputField(BaseField):
    def __init__(
        self,
        y: int,
        window: window,
        name: str,
        id: str,
        validator: Callable[[int | str], int | str],
        value: str | None = None,
    ):
        super().__init__(y, window, name, id, validator, value)
        self.textwindow = window.derwin(1, 20, y, 15)
        init_pair(45, COLOR_WHITE, COLOR_BLACK)
        self.textwindow.bkgd(" ", color_pair(45))
        self.value: str = value or " "
        self.validator = validator
        self.editor = TextInput(self.textwindow, self.value, self._validator)

    def _validator(self, ch: str | int) -> str | int:
        if ch == KEY_RESIZE:
            self.value = self.editor.gather().strip()
        return ch

    def render(self) -> None:
        self.window.addstr(self.y, 1, f"{self.name}: ", A_BOLD)
        self.textwindow.move(0, 0)
        if self.value is None or len(self.value) == 0:
            self.value = " "
        self.editor.set_value(self.value)
        self.editor.render()
        # Editor().main(self.textwindow,self.value or "")

    def focus(self) -> None:
        self.editor.main()
        self.value = self.editor.gather().strip()