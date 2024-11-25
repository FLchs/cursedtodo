import curses
from typing import Callable, Tuple


class Buffer:
    def __init__(self, value: str | None):
        self.line: str = value if value is not None else ""

    def set_value(self, line: str) -> None:
        self.line = line

    def insert(self, cursor: "Cursor", string: str) -> None:
        col = cursor.col
        self.line = self.line[:col] + string + self.line[col:]

    def delete(self, cursor: "Cursor") -> None:
        col = cursor.col
        if col < len(self.line):
            current = self.line
            if col < len(current):
                self.line = current[:col] + current[col + 1 :]


class Cursor:
    def __init__(self, row: int = 0, col: int = 0) -> None:
        self.row = row
        self._col = col

    @property
    def col(self) -> int:
        return self._col

    @col.setter
    def col(self, col: int) -> None:
        self._col = col

    def left(self) -> None:
        if self.col > 0:
            self.col -= 1

    def right(self, buffer: Buffer) -> None:
        if self.col < len(buffer.line):
            self.col += 1


class Window:
    def __init__(self, n_cols: int) -> None:
        self.n_cols = n_cols
        self.col = 0

    def translate(self, cursor: Cursor) -> Tuple[int, int]:
        return 0, cursor.col - self.col

    def horizontal_scroll(
        self, cursor: Cursor, left_margin: int = 5, right_margin: int = 0
    ) -> None:
        page_n_cols = self.n_cols - left_margin - right_margin
        n_pages = max((cursor.col - left_margin) // page_n_cols, 0)
        self.col = n_pages * page_n_cols


def right(window: Window, buffer: Buffer, cursor: Cursor) -> None:
    cursor.right(buffer)
    window.horizontal_scroll(cursor)


def left(window: Window, cursor: Cursor) -> None:
    cursor.left()
    window.horizontal_scroll(cursor)


class TextInput:
    def __init__(
        self,
        stdscr: curses.window,
        value: str | None,
        validator: Callable[[int | str], int | str],
    ) -> None:
        self.validator = validator
        self.buffer = Buffer(value)
        self.lines, self.cols = stdscr.getmaxyx()
        self.stdscr = stdscr
        self.window = Window(self.cols - 3)
        self.cursor = Cursor()

    def set_value(self, lines: str) -> None:
        self.buffer.set_value(lines)

    def gather(self) -> str:
        return "".join(self.buffer.line)

    def render(self) -> None:
        buffer = self.buffer
        window = self.window
        cursor = self.cursor
        self.stdscr.erase()

        line = buffer.line
        if window.col > 0:
            line = "«" + line[window.col + 1 :]
        if len(line) > window.n_cols:
            line = line[: window.n_cols - 1] + "»"
        self.stdscr.addstr(0, 0, line)
        self.stdscr.move(*window.translate(cursor))

    def main(self) -> None:
        buffer = self.buffer
        window = self.window
        self.stdscr.keypad(True)
        cursor = self.cursor
        cursor.col = min(len(self.buffer.line), window.n_cols)
        curses.curs_set(True)
        while True:
            self.render()
            k = self.stdscr.get_wch()
            if not self.validator(k):
                break
            if k == curses.KEY_LEFT:
                cursor.left()
                window.horizontal_scroll(cursor)
            elif k == curses.KEY_RIGHT:
                cursor.right(buffer)
                window.horizontal_scroll(cursor)
            elif k == "\n":
                pass
            elif k == curses.KEY_BACKSPACE:
                if (cursor.row, cursor.col) > (0, 0):
                    left(window, cursor)
                    buffer.delete(cursor)
            elif k == '\x0e' or k == '\x1b' or k == "\t":
                break
            elif isinstance(k, str):
                if k == "\t":
                    k = "  "
                buffer.insert(cursor, k)
                for _ in k:
                    right(window, buffer, cursor)
