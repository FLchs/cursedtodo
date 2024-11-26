from collections.abc import Callable
from curses import A_BOLD, COLOR_WHITE, KEY_RESIZE, color_pair, init_pair, window
import curses

from cursedtodo.utils.editor import Editor
from cursedtodo.views.form.base_field import BaseField


class TextArea(BaseField):
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
        self.textwindow = window.derwin(8, 100, y+1, 1)
        init_pair(45, COLOR_WHITE, curses.COLOR_BLACK)
        self.textwindow.bkgd(' ', color_pair(45))
        self.value: str = str(value)
        self.validator = validator
        self.editor = Editor(self.textwindow, self.value or "", self._validator)

    def _validator(self, ch: str | int) -> str | int:
        if ch == KEY_RESIZE:
            self.value = self.editor.gather()
        self.validator(ch)
        return ch

    def render(self) -> None:
        self.window.addstr(self.y, 1, f"{self.name}: ", A_BOLD)
        self.textwindow.move(0, 0)
        self.editor.set_value(self.value or "")
        self.editor.render()
        # Editor().main(self.textwindow,self.value or "")

    def focus(self) -> None:
        self.editor.main()
        self.value = self.editor.gather()
