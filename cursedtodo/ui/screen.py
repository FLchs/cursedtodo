import curses
from dataclasses import dataclass, field


@dataclass
class Screen:
    num_rows: int = field(init=False, repr=False)
    num_cols: int = field(init=False, repr=False)
    screen: curses.window = field(init=False, repr=False)

    def refresh(self):
        self.screen = curses.initscr()
        # Initialize color in a separate step
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)
        curses.curs_set(0)

        self.num_rows, self.num_cols = self.screen.getmaxyx()

        self.screen.addstr(self.num_rows - 1, 0, "q:quit | o:change order")

        curses.cbreak()
        curses.noecho()
        self.screen.keypad(True)
        self.screen.refresh()

    def __post_init__(self):
        self.refresh()
