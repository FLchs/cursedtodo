from cursedtodo.controlers.base_controller import Controller
from curses import KEY_RESIZE

from cursedtodo.models.todo import Todo
from cursedtodo.views.create_todo_view import CreateTodoView


class CreateTodoController(Controller):
    def run(self) -> None:
        self.view = CreateTodoView(self)
        self.window.clear()
        self.view.render()
        self.view.main_loop()

    def handle_key(self, key: int) -> bool:
        if key == KEY_RESIZE:
            self.view.render()
        if key == 27:
            return True
        return False

    def create_todo(self, data: dict[str, str]) -> None:
        summary = data.get("summary",  "")
        description = data.get("description", "")
        categories = (data.get("categories") or "").split(",")
        list = data.get("list", "").strip()
        priority = int(data.get("priority", "0"))
        location = data.get("location", "")

        todo = Todo(
            "",
            summary,
            description,
            categories,
            list,
            None,
            priority,
            None,
            None,
            location,
        )
        todo.save()
