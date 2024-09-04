from curses import window

from cursedtodo.models.todo import Todo
from cursedtodo.views.todo.edit import EditTodoView


class EditTodoPresenter:
    def __init__(self, stdscr: window, view: EditTodoView, todo: Todo | None):
        self.stdscr = stdscr
        self.view = view
        self.todo = todo

    def run(self):
        self.view.init(self)
        result = self.view.render()
        if self.todo is not None and result is not None:
            # TODO: Save the modified todo
            self.todo.summary = result[0]
            self.todo.priority = int(result[1])
            self.todo.list = result[2]
            self.todo.save()
