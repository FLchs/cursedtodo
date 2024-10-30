from curses import window
import curses.ascii
from typing import Callable


class Textbox:
    def __init__(self, win: window, insert_mode: bool = False) -> None:
        self.win = win
        self.insert_mode = insert_mode
        self._update_max_yx()
        self.stripspaces = 1
        self.lastcmd: int | str | None = None
        win.keypad(True)

    def _update_max_yx(self) -> None:
        maxy, maxx = self.win.getmaxyx()
        self.maxy = maxy - 1
        self.maxx = maxx - 1

    def _end_of_line(self, y: int) -> int:
        """Go to the location of the first blank on the given line,
        returning the index of the last non-blank character."""
        self._update_max_yx()
        last = self.maxx
        while True:
            if curses.ascii.ascii(self.win.inch(y, last)) != curses.ascii.SP:
                last = min(self.maxx, last + 1)
                break
            elif last == 0:
                break
            last = last - 1
        return last

    def _insert_printable_char(self, ch: str | int) -> None:
        self._update_max_yx()
        (y, x) = self.win.getyx()
        backyx = None
        while y < self.maxy or x < self.maxx:
            oldch = None
            if self.insert_mode:
                oldch = self.win.inch()
            # The try-catch ignores the error we trigger from some curses
            # versions by trying to write into the lowest-rightmost spot
            # in the window.
            try:
                self.win.addch(ch)
            except curses.error:
                pass
            if not self.insert_mode or oldch is None or not curses.ascii.isprint(oldch):
                break
            ch = oldch
            (y, x) = self.win.getyx()
            # Remember where to put the cursor back since we are in insert_mode
            if backyx is None:
                backyx = y, x

        if backyx is not None:
            self.win.move(*backyx)

    def do_command(self, ch: int | str) -> int:
        "Process a single editing command."
        self._update_max_yx()
        (y, x) = self.win.getyx()
        self.lastcmd = ch

        if isinstance(ch, str) and 31 < ord(ch):
            if y < self.maxy or x < self.maxx:
                self._insert_printable_char(ch)
        else:
            if ch == "\n":
                return 0
            elif ch in (
                curses.ascii.STX,
                curses.KEY_LEFT,
                curses.ascii.BS,
                curses.KEY_BACKSPACE,
                curses.ascii.DEL,
            ):
                if x > 0:
                    self.win.move(y, x - 1)
                elif y == 0:
                    pass
                elif self.stripspaces:
                    self.win.move(y - 1, self._end_of_line(y - 1))
                else:
                    self.win.move(y - 1, self.maxx)
                if ch in (curses.ascii.BS, curses.KEY_BACKSPACE, curses.ascii.DEL):
                    self.win.delch()
            elif ch in (curses.ascii.ACK, curses.KEY_RIGHT):  # ^f
                if x < self.maxx:
                    self.win.move(y, x + 1)
                elif y == self.maxy:
                    pass
                else:
                    self.win.move(y + 1, 0)
        return 1

    def gather(self) -> str:
        "Collect and return the contents of the window."
        result = ""
        self._update_max_yx()
        for y in range(self.maxy + 1):
            self.win.move(y, 0)
            stop = self._end_of_line(y)
            if stop == 0 and self.stripspaces:
                continue
            for x in range(self.maxx + 1):
                if self.stripspaces and x > stop:
                    break
                result = result + chr(self.win.inch(y, x))
            if self.maxy > 0:
                result = result + "\n"
        return result

    def edit(self, validate: Callable[[int | str], int | str ]| None = None) -> str:
        "Edit in the widget window and collect the results."
        while 1:
            self.win.keypad(True)
            ch: int | str = self.win.get_wch()
            if validate:
                ch = validate(ch)
            if not ch:
                continue
            if not self.do_command(ch):
                break
            self.win.refresh()
        return self.gather()
