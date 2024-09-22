from curses import newwin, panel


class BaseView:
    def __init__(self, screen, presenter):
        self.screen = screen
        self.presenter = presenter
        self.rows, self.cols = self.screen.getmaxyx()
        self.window = newwin(self.rows, self.cols, 0, 0)
        self.panel = panel.new_panel(self.window)

    def show(self):
        raise NotImplementedError("Each view must implement a show method.")
