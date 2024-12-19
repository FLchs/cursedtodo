from datetime import datetime
from os import name
from typing import Any
from cursedtodo.config import Config
from cursedtodo.controlers.base_controller import Controller
from curses import KEY_RESIZE

from cursedtodo.models.todo import Todo
from cursedtodo.models.todo_repository import TodoRepository
from cursedtodo.utils.formater import Formater
from cursedtodo.utils.validator import Validator
from cursedtodo.views.edit_todo_view import EditTodoView


class EditTodoController(Controller):
    def run(self, todo: Todo | None = None) -> None:
        self.todo = todo
        self.view = EditTodoView(self)
        self.window.clear()
        self.view.render()
        self.view.main_loop()

    def handle_key(self, key: int) -> bool:
        if key == KEY_RESIZE:
            self.view.render()
        if key == 27:
            return True
        return False

    def create_or_update_todo(self, data: dict[str, Any]) -> None:
        summary = Validator.validate(data.get("summary"), str)
        description = Validator.validate(data.get("description"), str)
        location = Validator.validate(data.get("location"), str)
        categories = Validator.validate_list(data.get("categories"), str)
        list = data.get("list", "")
        priority = Formater.parse_priority(data.get("priority"))
        due = Validator.validate_optional(data.get("due"), datetime)
        calendar = next(filter(lambda cal: cal.name == list, Config.calendars))

        if self.todo is None:
            todo = Todo(
                "",
                calendar,
                summary,
                description,
                categories,
                None,
                priority,
                None,
                due,
                location,
            )
        else:
            todo = self.todo
            todo.calendar = calendar
            todo.summary = summary
            todo.description = description
            todo.categories = categories
            todo.due = due
            todo.location = location
            todo.priority = priority
        TodoRepository.save(todo)
