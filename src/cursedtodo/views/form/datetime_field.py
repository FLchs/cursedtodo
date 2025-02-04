from collections.abc import Callable
from curses import A_BOLD, KEY_RESIZE, window
from datetime import datetime
from cursedtodo.utils.colors import WHITE
from cursedtodo.utils.textinput import TextInput
from cursedtodo.utils.time import TimeUtil
from cursedtodo.views.form.base_field import BaseField


class DatetimeField(BaseField):
    def __init__(
        self,
        y: int,
        window: window,
        id: str,
        name: str,
        validator: Callable[[int | str], int | str],
    ):
        super().__init__(y, window, name, id, validator)
        self.value: datetime | None = None
        self.textwindow = window.derwin(1, 20, y, 15)
        self.textwindow.bkgd(" ", WHITE)
        self.validator = validator
        self.editor = TextInput(self.textwindow, "", self._validator)

    def _validator(self, ch: str | int) -> str | int:
        if ch == KEY_RESIZE:
            self.value = TimeUtil.parse_to_datetime(self.editor.gather())
        self.validator(ch)
        return ch

    def render(self) -> None:
        self.textwindow.erase()
        if self.name != "":
            self.window.addstr(self.y, 1, f"{self.name}: ", A_BOLD)
        self.textwindow.move(0, 0)
        if self.value is not None:
            value = TimeUtil.datetime_format(self.value)
            self.editor.set_value(value)
        self.editor.render()
        self.textwindow.refresh()

    def focus(self) -> None:
        self.editor.main()
        value = self.editor.gather()
        if value is None or len(value) == 0:
            return
        self.value = TimeUtil.parse_to_datetime(self.editor.gather())
