from collections.abc import Callable
from curses import A_BOLD, KEY_RESIZE, window

from cursedtodo.utils.formater import Formater
from cursedtodo.utils.selectinput import SelectInput
from cursedtodo.views.form.base_field import BaseField


class PriorityField(BaseField):
    def __init__(
        self,
        y: int,
        window: window,
        name: str,
        id: str,
        validator: Callable[[int | str], int | str],
    ):
        super().__init__(y, window, name, id, validator, None)
        self.priorities = [p.value for p in Formater.priorities]
        self.value: str = self.priorities[0]
        self.textwindow = window.derwin(1, 25, y, 15)
        self.validator = validator
        self.editor = SelectInput(self.textwindow, self.priorities, self._validator, False)

    def _validator(self, ch: str | int) -> str | int:
        if ch == KEY_RESIZE:
            self.value = self.editor.gather().strip()
        self.validator(ch)
        return ch

    def render(self) -> None:
        self.window.addstr(self.y, 1, f"{self.name}: ", A_BOLD)
        self.textwindow.move(0, 0)
        if self.value is not None:
            self.editor.set_value(self.value)
        self.editor.render()

    def focus(self) -> None:
        self.editor.main()
        self.value = self.editor.gather().strip()
