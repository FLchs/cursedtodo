import curses
from typing import Callable, Tuple, Union


class Buffer:
    def __init__(self, lines: str | None):
        self.lines = lines.split() if lines is not None else [""]

    def set_value(self, lines: str) -> None:
        self.lines = lines.splitlines()

    def __len__(self) -> int:
        return len(self.lines)

    def __getitem__(self, index: Union[int, slice]) -> str | list[str]:
        return self.lines[index]

    @property
    def bottom(self) -> int:
        return len(self) - 1

    def insert(self, cursor: "Cursor", string: str) -> None:
        row, col = cursor.row, cursor.col
        if len(self.lines) > 0:
            current = self.lines.pop(row)
            new = current[:col] + string + current[col:]
        else:
            new = string
        self.lines.insert(row, new)

    def split(self, cursor: "Cursor") -> None:
        row, col = cursor.row, cursor.col
        current = self.lines.pop(row)
        self.lines.insert(row, current[:col])
        self.lines.insert(row + 1, current[col:])

    def delete(self, cursor: "Cursor") -> None:
        row, col = cursor.row, cursor.col
        if (row, col) < (self.bottom, len(self[row])):
            current = self.lines.pop(row)
            if col < len(current):
                new = current[:col] + current[col + 1 :]
                self.lines.insert(row, new)
            else:
                next = self.lines.pop(row)
                new = current + next
                self.lines.insert(row, new)


class Cursor:
    def __init__(self, row: int = 0, col: int = 0, col_hint: int | None = None) -> None:
        self.row = row
        self._col = col
        self._col_hint = col if col_hint is None else col_hint

    @property
    def col(self) -> int:
        return self._col

    @col.setter
    def col(self, col: int) -> None:
        self._col = col
        self._col_hint = col

    def up(self, buffer: Buffer) -> None:
        if self.row > 0:
            self.row -= 1
            self._clamp_col(buffer)

    def down(self, buffer: Buffer) -> None:
        if self.row < buffer.bottom:
            self.row += 1
            self._clamp_col(buffer)

    def left(self, buffer: Buffer) -> None:
        if self.col > 0:
            self.col -= 1
        elif self.row > 0:
            self.row -= 1
            self.col = len(buffer[self.row])

    def right(self, buffer: Buffer) -> None:
        if self.col < len(buffer[self.row]):
            self.col += 1
        elif self.row < buffer.bottom:
            self.row += 1
            self.col = 0

    def _clamp_col(self, buffer: Buffer) -> None:
        self._col = min(self._col_hint, len(buffer[self.row]))


class Window:
    def __init__(self, n_rows: int, n_cols: int, row: int = 0, col: int = 0) -> None:
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.row = row
        self.col = col

    @property
    def bottom(self) -> int:
        return self.row + self.n_rows - 1

    def up(self, cursor: Cursor) -> None:
        if cursor.row == self.row - 1 and self.row > 0:
            self.row -= 1

    def down(self, buffer: Buffer, cursor: Cursor) -> None:
        if cursor.row == self.bottom + 1 and self.bottom < buffer.bottom:
            self.row += 1

    def translate(self, cursor: Cursor) -> Tuple[int, int]:
        return cursor.row - self.row, cursor.col - self.col

    def horizontal_scroll(
        self, cursor: Cursor, left_margin: int = 5, right_margin: int = 2
    ) -> None:
        n_pages = cursor.col // (self.n_cols - right_margin)
        self.col = max(n_pages * self.n_cols - right_margin - left_margin, 0)


def right(window: Window, buffer: Buffer, cursor: Cursor) -> None:
    cursor.right(buffer)
    window.down(buffer, cursor)
    window.horizontal_scroll(cursor)


def left(window: Window, buffer: Buffer, cursor: Cursor) -> None:
    cursor.left(buffer)
    window.up(cursor)
    window.horizontal_scroll(cursor)


class Editor:
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
        self.window = Window(self.lines - 1, self.cols - 2)
        self.cursor = Cursor()

    def set_value(self, lines: str) -> None:
        self.buffer.set_value(lines)

    def gather(self) -> str:
        return "\n".join(self.buffer.lines)

    def render(self) -> None:
        # TODO: Improve resize
        buffer = self.buffer
        window = self.window
        cursor = self.cursor
        self.stdscr.erase()
        if len(buffer.lines) > window.n_rows:
            y_pos = min(
                (window.row) / (len(buffer.lines) - window.n_rows) * window.n_rows,
                window.n_rows,
            )
            for row in range(window.n_rows + 1):
                if row == round(y_pos):
                    self.stdscr.addch(row, window.n_cols, "█")
                else:
                    self.stdscr.addch(row, window.n_cols, "│")

        for row, line in enumerate(buffer[window.row : window.row + window.n_rows]):
            if row == cursor.row - window.row and window.col > 0:
                line = "«" + line[window.col + 1 :]
            if len(line) > window.n_cols:
                self.stdscr.addstr(window.n_rows, 5, f"{len(line)}/{window.n_cols}")
                line = line[: window.n_cols - 1] + "»"
            self.stdscr.addstr(row, 0, line)
            self.stdscr.move(*window.translate(cursor))

    def main(self) -> None:
        buffer = self.buffer
        window = self.window
        self.stdscr.keypad(True)
        cursor = self.cursor
        curses.curs_set(True)
        while True:
            self.render()
            k = self.stdscr.get_wch()
            if not self.validator(k):
                break
            if k == "q":
                break
            elif k == curses.KEY_UP:
                cursor.up(buffer)
                window.up(cursor)
                window.horizontal_scroll(cursor)
            elif k == curses.KEY_DOWN:
                cursor.down(buffer)
                window.down(buffer, cursor)
                window.horizontal_scroll(cursor)
            elif k == curses.KEY_LEFT:
                cursor.left(buffer)
                window.up(cursor)
                window.horizontal_scroll(cursor)
            elif k == curses.KEY_RIGHT:
                cursor.right(buffer)
                window.down(buffer, cursor)
                window.horizontal_scroll(cursor)
            elif k == "\n":
                buffer.split(cursor)
                right(window, buffer, cursor)
            elif k == curses.KEY_BACKSPACE:
                if (cursor.row, cursor.col) > (0, 0):
                    left(window, buffer, cursor)
                    buffer.delete(cursor)
            elif k == curses.KEY_BTAB:
                buffer.insert(cursor, "  ")
                right(window, buffer, cursor)
                right(window, buffer, cursor)
            elif k == "\t":
                break
            elif isinstance(k, str):
                buffer.insert(cursor, k)
                for _ in k:
                    right(window, buffer, cursor)
