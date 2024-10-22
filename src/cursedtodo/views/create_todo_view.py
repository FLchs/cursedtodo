from __future__ import annotations

from curses import KEY_RESIZE
from typing import TYPE_CHECKING, Dict


from cursedtodo.utils.window_utils import add_borders
from cursedtodo.views.base_view import BaseView
from cursedtodo.views.form.Button import Button
from cursedtodo.views.form.Field import Field

if TYPE_CHECKING:
    from cursedtodo.controlers.create_todo_controller import CreateTodoController


class CreateTodoView(BaseView):
    def __init__(self, controller: CreateTodoController) -> None:
        super().__init__(controller)
        self.controller = controller
        self.height, self.length = self.window.getmaxyx()
        self.fields: list[Field] = [
            Field(2, self.window, "List", "list", self.validator),
            Field(3, self.window, "Summary", "summary", self.validator),
            Field(4, self.window, "Priority", "priority", self.validator),
            Field(5, self.window, "Due", "due", self.validator),
            Field(6, self.window, "Categories", "categories", self.validator),
            Field(7, self.window, "Location", "location", self.validator),
            Field(9, self.window, "Description", "description", self.validator),
        ]
        self.save_button = Button(self.window, 10, 1, "Save", self.save, self.validator)
        self.cancel_button = Button(
            self.window, 10, 6, "Cancel", self.cancel, self.validator
        )

    def render(self) -> None:
        self.height, self.length = self.window.getmaxyx()
        for field in self.fields:
            field.save()
        self.window.erase()
        self.window.border()
        add_borders(self.window)
        self.window.addstr(self.height - 1, 5, " tab: next field | esc: cancel ")
        self.window.addstr(0, 5, " New todo ")
        # self.window.addstr(1, 1, "Calendar: ")
        for field in self.fields:
            field.render()
        self.save_button.render()
        self.cancel_button.render()
        self.window.refresh()

    def save(self) -> bool:
        values: Dict[str, str] = {}
        for field in self.fields:
            values.update({field.id: field.value})
        self.controller.create_todo(values)
        return True

    def cancel(self) -> bool:
        return True

    def validator(self, ch: int) -> int:
        if ch == KEY_RESIZE:
            self.render()
            return ch
        elif ch == 9:
            return 7
        else:
            return ch

    def main_loop(self) -> None:
        index = 0
        self.window.refresh()
        while True:
            if index < len(self.fields):
                self.fields[index].focus()
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
