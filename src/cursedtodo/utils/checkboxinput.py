import curses
from typing import Callable


class CheckboxInput:
    def __init__(
        self,
        stdscr: curses.window,
        validator: Callable[[int | str], int | str],
        value: bool = False,
    ) -> None:
        self.validator = validator
        self.lines, self.cols = stdscr.getmaxyx()
        self.stdscr = stdscr
        self.value = value

    def set_value(self, value: bool) -> None:
        self.value = value

    def gather(self) -> bool:
        return self.value

    def render(self, active: bool = False) -> None:
        self.stdscr.erase()
        if self.value:
            self.stdscr.addstr("[x]", curses.A_REVERSE if active else curses.A_NORMAL)
        else:
            self.stdscr.addstr("[ ]", curses.A_REVERSE if active else curses.A_NORMAL)

    def main(self) -> None:
        curses.curs_set(False)
        self.stdscr.keypad(True)
        while True:
            self.render(True)
            k = self.stdscr.get_wch()
            if not self.validator(k):
                break
            elif k == " ":
                self.value = not self.value
            elif k == "\x0e" or k == "\x1b" or k == "\t":
                break
        self.stdscr.chgat(0, 0, self.cols - 1, curses.A_NORMAL)
        self.stdscr.refresh()
