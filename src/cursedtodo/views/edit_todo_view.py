from __future__ import annotations

from curses import KEY_RESIZE
from typing import TYPE_CHECKING, Any, Dict


from cursedtodo.config import Config
from cursedtodo.models.todo_repository import TodoRepository
from cursedtodo.utils.window_utils import add_borders, draw_line
from cursedtodo.views.base_view import BaseView
from cursedtodo.views.form.Button import Button
from cursedtodo.views.form.base_field import BaseField
from cursedtodo.views.form.categories_field import CategoriesField
from cursedtodo.views.form.datetime_field import DatetimeField
from cursedtodo.views.form.priority_field import PriorityField
from cursedtodo.views.form.select_field import SelectField
from cursedtodo.views.form.textarea_field import TextArea
from cursedtodo.views.form.textinput_field import TextInputField

if TYPE_CHECKING:
    from cursedtodo.controlers.edit_todo_controller import EditTodoController


class EditTodoView(BaseView):
    def __init__(self, controller: EditTodoController) -> None:
        super().__init__(controller)
        self.controller = controller
        self.height, self.length = self.window.getmaxyx()
        todo = self.controller.todo
        lists = TodoRepository.get_lists_names()
        default_list = Config.ui.default_calendar

        self.fields: Dict[str, BaseField] = {
            "list": SelectField(
                2, self.window, "List", "list", lists, self.validator, default_list
            ),
            "summary": TextInputField(
                3, self.window, "Summary", "summary", self.validator, ""
            ),
            "priority": PriorityField(
                4, self.window, "Priority", "priority", self.validator
            ),
            "due": DatetimeField(5, self.window, "due", self.validator),
            "categories": CategoriesField(6, self.window, "categories", self.validator),
            "location": TextInputField(
                7, self.window, "Location", "location", self.validator
            ),
            "description": TextArea(
                9, self.window, "Description", "description", self.validator, ""
            ),
        }
        if todo:
            for key, field in self.fields.items():
                if key == "list":
                    field.value = todo.calendar.name
                else:
                    field.value = getattr(todo, key)
        self.save_button = Button(
            self.window, self.height - 2, 1, "[ Save ]", self.save, self.validator
        )
        self.cancel_button = Button(
            self.window, self.height - 2, 10, "[ Cancel ]", self.cancel, self.validator
        )

    def render(self) -> None:
        self.height, self.length = self.window.getmaxyx()
        self.window.erase()
        self.window.border()
        add_borders(self.window)
        self.window.addstr(self.height - 1, 5, " tab: next field ")
        self.window.addstr(0, 5, " Edit todo ")
        draw_line(self.window, 8, self.length)
        for field in self.fields.values():
            field.render()
        self.save_button.render(self.height - 2, 1)
        self.cancel_button.render(self.height - 2, 10)
        self.window.refresh()

    def save(self) -> bool:
        values: Dict[str, Any] = {}
        for field in self.fields.values():
            values.update({field.id: field.value})
        self.controller.create_or_update_todo(values)
        return True

    def cancel(self) -> bool:
        return True

    def validator(self, ch: int | str) -> int | str:
        if ch == KEY_RESIZE:
            self.render()
        return ch

    def main_loop(self) -> None:
        index = 0
        fields = list(self.fields.values())
        self.window.refresh()
        while True:
            if index < len(self.fields):
                fields[index].focus()
                index += 1
            elif index == len(self.fields):
                if self.save_button.focus():
                    break
                index += 1
            elif index == len(self.fields) + 1:
                if self.cancel_button.focus():
                    break
                index += 1
            else:
                index = 0
