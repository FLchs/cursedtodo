from collections.abc import Callable
from curses import A_BOLD, KEY_RESIZE, window

from cursedtodo.utils.checkboxinput import CheckboxInput
from cursedtodo.views.form.base_field import BaseField


class CheckboxField(BaseField):
    def __init__(
        self,
        y: int,
        window: window,
        name: str,
        id: str,
        validator: Callable[[int | str], int | str],
        default_value: bool = False,
    ):
        super().__init__(y, window, name, id, validator, None)
        self.value: bool = default_value
        self.textwindow = window.derwin(1, 25, y, 15)
        self.validator = validator
        self.editor = CheckboxInput(self.textwindow, self._validator)

    def _validator(self, ch: str | int) -> str | int:
        if ch == KEY_RESIZE:
            self.value = self.editor.gather()
        self.validator(ch)
        return ch

    def render(self) -> None:
        self.window.addstr(self.y, 1, f"{self.name}: ", A_BOLD)
        self.textwindow.move(0, 0)
        self.editor.set_value(self.value)
        self.editor.render()

    def focus(self) -> None:
        self.editor.main()
        self.value = self.editor.gather()
