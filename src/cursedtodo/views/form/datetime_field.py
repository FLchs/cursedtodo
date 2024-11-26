from collections.abc import Callable
from curses import A_BOLD, COLOR_WHITE, KEY_RESIZE, color_pair, init_pair, window
import curses
from datetime import datetime
from cursedtodo.utils.textinput import TextInput
from cursedtodo.utils.time import datetime_format, parse_to_datetime
from cursedtodo.views.form.base_field import BaseField

class DatetimeField(BaseField):
    def __init__(
        self,
        y: int,
        window: window,
        id: str,
        validator: Callable[[int | str], int | str],
    ):
        super().__init__(y, window, id, id, validator)
        self.value: datetime | None = None
        self.textwindow = window.derwin(1, 20, y, 15)
        init_pair(45, COLOR_WHITE, curses.COLOR_BLACK)
        self.textwindow.bkgd(' ', color_pair(45))
        self.validator = validator
        self.editor = TextInput(self.textwindow, "", self._validator)

    def _validator(self, ch: str | int) -> str | int:
        if ch == KEY_RESIZE:
            try:
                self.value = parse_to_datetime(self.editor.gather())
            except ValueError:
            # TODO: we still need to be nice to the user there
                pass
        self.validator(ch)
        return ch

    def render(self) -> None:
        self.textwindow.erase()
        self.window.addstr(self.y, 1, f"{self.id.capitalize()}: ", A_BOLD)
        self.textwindow.move(0, 0)
        if self.value is not None:
            value = datetime_format(self.value) 
            self.editor.set_value(value)
        self.editor.render()
        self.textwindow.refresh()

    def focus(self) -> None:
        self.editor.main()
        value = self.editor.gather()
        if value is None or len(value) == 0:
            return
        try:
            self.value = parse_to_datetime(self.editor.gather())
        except Exception:
            self.editor.set_value(datetime_format(datetime.now()))
            self.editor.render()
            self.textwindow.refresh()
