from collections.abc import Callable
from curses import A_BOLD, KEY_RESIZE, curs_set, window

from cursedtodo.utils.textpad import Textbox
from cursedtodo.views.form.base_field import BaseField


class TextField(BaseField):
    def __init__(
        self,
        y: int,
        window: window,
        name: str,
        id: str,
        validator: Callable[[int | str], int | str],
        value: str | None = None,
    ):
        super().__init__(y, window,name,id,validator,value)
        self.textwindow = window.derwin(1, 100, y, 15)
        self.textbox = Textbox(self.textwindow, insert_mode=True)
        self.value = str(value)
        self.validator = validator

    def _validator(self, ch: str | int) -> str | int:
        if ch == KEY_RESIZE:
            self.value = self.textbox.gather().strip()
        if ch == "\t":
            return u"\u001F"
        return self.validator(ch)

    def render(self) -> None:
        self.window.addstr(self.y, 1, f"{self.name}: ", A_BOLD)
        self.textwindow.move(0, 0)
        if self.value:
            try:
                self.textwindow.addstr(self.value.strip())
            except Exception:
                pass

    def focus(self) -> None:
        curs_set(1)
        self.textbox.edit(self._validator)
        self.value = self.textbox.gather()
