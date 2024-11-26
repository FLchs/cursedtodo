import curses
from typing import Callable


class Cursor:
    def __init__(self, values_nb: int, loop: bool) -> None:
        self.value = 0
        self.values_nb = values_nb - 1
        self.loop = loop

    def left(self) -> None:
        if self.value > 0:
            self.value -= 1
        elif self.loop:
            self.value = self.values_nb

    def right(self) -> None:
        if self.value < self.values_nb:
            self.value += 1
        elif self.loop:
            self.value = 0


class SelectInput:
    def __init__(
        self,
        stdscr: curses.window,
        values: list[str],
        validator: Callable[[int | str], int | str],
        loop: bool = True
    ) -> None:
        self.validator = validator
        self.lines, self.cols = stdscr.getmaxyx()
        self.stdscr = stdscr
        self.values = values
        self.cursor = Cursor(len(self.values), loop)
        self.cursor.value = 0

    def set_value(self, value: str) -> None:
        try:
            if value not in self.values:
                self.cursor.value = min(int(value), len(self.values)-1)
            else:
                self.cursor.value = self.values.index(value)
        except ValueError:
            self.values.append(value)
            self.cursor.value = len(self.values) - 1
        except IndexError:
            self.cursor.value = 0

    def gather(self) -> str:
        return self.values[self.cursor.value]

    def render(self, active: bool = False) -> None:
        cursor = self.cursor
        self.stdscr.erase()
        self.stdscr.addstr(0, 0, "< ")
        self.stdscr.addstr(f"{self.values[cursor.value]}", curses.A_REVERSE if active else curses.A_NORMAL)
        self.stdscr.addstr(" >")

    def main(self) -> None:
        cursor = self.cursor
        curses.curs_set(False)
        self.stdscr.keypad(True)
        while True:
            self.render(True)
            k = self.stdscr.get_wch()
            if not self.validator(k):
                break
            if k == curses.KEY_LEFT or k == "h":
                cursor.left()
            elif k == curses.KEY_RIGHT or k == "l":
                cursor.right()
            elif k == "\x0e" or k == "\x1b" or k == "\t":
                break
        self.stdscr.chgat(0, 0, self.cols - 1, curses.A_NORMAL)
        self.stdscr.refresh()
