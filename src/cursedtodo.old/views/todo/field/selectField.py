from curses import A_NORMAL, A_REVERSE, curs_set, newwin

from cursedtodo.views.todo.field.field import Field


class SelectField(Field):
    def __init__(self, name: str, id: int, validator, values: list[str], selected: str):
        super().__init__(name, id, validator)
        try:
            self.selected = values.index(selected)
        except ValueError:
            self.selected = 0
        self.values = values
        self.validator = validator

    def render(self):
        id = self.id
        name = self.name
        self.win = newwin(1, 40, id + 1, 1)
        self.win.addstr(0, 0, name + ": " + self.values[self.selected])
        self.win.refresh()

    def gather(self):
        name = self.name
        win = self.win
        curs_set(0)
        while True:
            win.move(0, len(name) + 2)  # Move cursor to the start of the string
            win.clrtoeol()  # Clear to the end of the line
            win.refresh()
            win.addstr(0, len(name) + 2, self.values[self.selected], A_REVERSE)
            k = win.getch()
            if k == ord("j"):
                self.selected = (
                    self.selected + 1 if self.selected + 1 < len(self.values) else 0
                )
            elif k == ord("k"):
                self.selected = (
                    self.selected - 1 if self.selected > 0 else len(self.values) - 1
                )
            else:
                win.move(0, len(name) + 2)  # Move cursor to the start of the string
                win.chgat(40, A_NORMAL)
                win.refresh()
                self.validator(k)
                return self.values[self.selected]
