from cursedtodo.controlers.base_controller import Controller
from curses import KEY_RESIZE

from cursedtodo.models.todo import Todo
from cursedtodo.views.view_todo_view import ViewTodoView

class ViewTodoController(Controller):



    def run(self, todo: Todo) -> None:
        self.todo = todo
        self.view = ViewTodoView(self)
        self.window.clear()
        self.view.render()
        self.view.main_loop()

    def handle_key(self, key: int) -> bool:
        if key == KEY_RESIZE:
            self.view.render()
        if key == ord("q"):
            return True
        return False
