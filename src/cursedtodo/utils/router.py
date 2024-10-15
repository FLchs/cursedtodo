from curses import window

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

    # def gotoB(self, data: str):
    #     bcontroller = BController(self.window, self, data = "nigga")
    #     bcontroller.run()
