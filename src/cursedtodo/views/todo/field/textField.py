from collections.abc import Callable
from curses import curs_set, newwin, textpad

from cursedtodo.views.todo.field.field import Field


class TextField(Field):
    def __init__(self, name: str, id: int, validator, value: str = ""):
        super().__init__(name, id, validator)
        self.value = value

    def render(self):
        id = self.id
        name = self.name
        value = self.value
        self.win = newwin(1, 50, id + 1, 12)
        sub = newwin(1, 25, id + 1, 1)
        sub.addstr(0, 0, name + ": ")
        sub.refresh()
        self.input_box = textpad.Textbox(self.win, insert_mode=True)
        self.win.addstr(value)
        self.win.refresh()

    def gather(self):
        curs_set(1)
        content = self.value
        win = self.win
        win.move(0, max(len(content), 0))
        self.input_box.edit(self.validator)
        self.value = self.input_box.gather().strip()
        return self.value
