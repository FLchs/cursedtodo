import curses
from dataclasses import dataclass, field

from cursedtodo.todo import Todo


@dataclass
class TodoList:
    rows: int
    cols: int
    selected: int = 0
    _window: curses.window = field(init=False, repr=False)

    col_widths = [19, 50, 50]
    col_headers = ["List", "Summary", "Priority"]

    def display_priority(self, priority):

        # Ensure the priority is within the valid range
        if priority < 0 or priority > 9:
            raise ValueError("Priority must be between 0 and 9")

        # Define words and colors based on priority
        words = [
            "Lowest",
            "Very Low",
            "Low",
            "Below Average",
            "Average",
            "Above Average",
            "High",
            "Very High",
            "Highest",
            "Critical",
        ]
        colors = [
            curses.COLOR_WHITE,
            curses.COLOR_BLUE,
            curses.COLOR_CYAN,
            curses.COLOR_GREEN,
            curses.COLOR_YELLOW,
            curses.COLOR_MAGENTA,
            curses.COLOR_RED,
            curses.COLOR_RED,
            curses.COLOR_RED,
            curses.COLOR_RED,
        ]

        # Initialize color pairs
        curses.start_color()
        for i, color in enumerate(colors):
            curses.init_pair(i + 10, color, curses.COLOR_BLACK)

        # Get the word and color for the given priority
        word = words[priority]
        color_pair = curses.color_pair(priority + 10)
        return word, color_pair

    def drawInit(self):
        window = self._window
        cols = self.cols
        window.clear()
        window.box()
        window.hline(2, 1, curses.ACS_HLINE, cols - 2)
        window.addch(2, 0, curses.ACS_LTEE)
        window.addch(2, cols - 1, curses.ACS_RTEE)
        window.attrset(curses.color_pair(0))
        window.addstr(1, int(cols / 2) - 4, "TODO")
        header_y = 1
        for id, name in enumerate(self.col_headers):
            window.addstr(3, header_y, name, curses.A_BOLD)
            header_y += int(self.col_widths[int(id)])
        window.refresh()

    def __post_init__(self):
        rows = self.rows
        cols = self.cols
        window = curses.newwin(rows, cols, 0, 0)
        self._window = window

    def select(self, id: int):
        self.selected = id

    def draw(self, data: list[Todo]):
        self.drawInit()
        for i, value in enumerate(data):
            if i < self.rows - 5:
                self._window.addstr(4 + i, 1, value.list)
                if self.selected == i:
                    self._window.addstr(4 + i, 20, value.summary, curses.A_STANDOUT)
                else:
                    self._window.addstr(4 + i, 20, value.summary)
                word, color = self.display_priority(value.priority)
                self._window.addstr(4 + i, 70, word, color)
        self._window.refresh()
