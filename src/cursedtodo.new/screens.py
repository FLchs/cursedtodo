from curses import window
from cursedtodo.models.todo import Todo
from cursedtodo.presenters.todolist import TodoListPresenter
from cursedtodo.views.todolist import TodoListView


class Screens:
    screen: window

    def __init__(self):
        pass

    def todo_list(self):
        view = TodoListView()
        presenter = TodoListPresenter(self.screen, view)
        presenter.run()

    def edit_todo(self, todo: Todo):
        pass

    def create_todo(self):
        pass

    def view_todo(self, todo: Todo):
        pass


navigator = Screens()
