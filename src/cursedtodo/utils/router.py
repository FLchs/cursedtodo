from curses import window

from cursedtodo.controlers.create_todo_controller import CreateTodoController
from cursedtodo.controlers.main_controller import MainController
from cursedtodo.controlers.view_todo_controller import ViewTodoController
from cursedtodo.models.todo import Todo


class Router:
    def __init__(self, window: window) -> None:
        self.window = window

    def route_main(self) -> None:
        acontroller = MainController(self)
        acontroller.run()

    def route_view_todo(self, todo: Todo) -> None:
        ViewTodoController(self).run(todo)

    def route_create_todo(self) -> None:
        CreateTodoController(self).run()
