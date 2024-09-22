from curses import A_BOLD, newwin

from cursedtodo.models.todo import Todo


class ShowTodoView:

    def __init__(self):
        pass

    def init(self, presenter):
        self.presenter = presenter
        self.todo: Todo = presenter.todo
        (self.rows, self.cols) = self.presenter.stdscr.getmaxyx()
        self.window = newwin(self.rows, self.cols, 0, 0)
        self.window.clear()
        self.window.box()

    def render(self=None):
        self.window.addstr(1, 1, "name :", A_BOLD)
        self.window.addstr(1, 15, self.todo.summary)
        self.window.addstr(2, 1, "list :", A_BOLD)
        self.window.addstr(2, 15, self.todo.list)
        self.window.addstr(3, 1, "priority :", A_BOLD)
        self.window.addstr(3, 15, str(self.todo.priority))
        if self.todo.description:
            self.window.addstr(4, 1, "description :", A_BOLD)
            self.window.addstr(4, 15, self.todo.description)
        if self.todo.categories:
            self.window.addstr(5, 1, "categories :", A_BOLD)
            self.window.addstr(5, 15, str(self.todo.categories or ""))
        return self.main_loop()

    def main_loop(self):
        self.window.getch()
