from curses import window

from cursedtodo.models.todo import Todo
from cursedtodo.views.todo.showtodo import ShowTodoView


class ShowTodoPresenter:
    def __init__(self, stdscr: window, view: ShowTodoView, todo: Todo | None):
        self.stdscr = stdscr
        self.view = view
        self.todo = todo

    def run(self):
        self.view.init(self)
        self.view.render()
