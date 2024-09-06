from curses import newwin, window


class Confirm:

    def __init__(self, text: str, window: window):
        self.text = text + " (Y/n)"
        self.height = 5
        self.rows, self.cols = window.getmaxyx()
        self.width = min(int(self.cols - 2), len(self.text) + 6)
        self.render()

    def render(self) -> bool:
        text = self.text
        win = newwin(
            self.height,
            self.width,
            int(self.rows / 2) - int(self.height / 2),
            int(self.cols / 2) - int(self.width / 2),
        )
        win.box()
        win.addstr(
            round(self.height / 2), int(self.width / 2) - int(len(text) / 2), text
        )

        yes = [10, ord("y"), ord("Y")]
        no = [27, ord("q"), ord("n"), ord("N")]

        while True:
            k = win.getch()
            if k in yes:
                return True
            elif k in no:
                return False
