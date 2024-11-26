from __future__ import annotations

from curses import (
    A_BOLD,
    COLOR_RED,
    init_pair,
)
from datetime import datetime
from typing import TYPE_CHECKING


from cursedtodo.utils.config import Config
from cursedtodo.utils.formater import Formater
from cursedtodo.utils.time import get_locale_tz
from cursedtodo.utils.window_utils import add_borders, draw_line
from cursedtodo.views.base_view import BaseView

if TYPE_CHECKING:
    from cursedtodo.controlers.view_todo_controller import ViewTodoController


class ViewTodoView(BaseView):
    def __init__(self, controller: ViewTodoController) -> None:
        super().__init__(controller)
        self.controller = controller

    def render(self) -> None:
        self.height, self.length = self.window.getmaxyx()
        todo = self.controller.todo
        self.window.erase()
        self.window.border()
        add_borders(self.window)
        self.window.addstr(self.height - 1, 5, " q: go back ")
        self.window.addstr(0, 5, todo.summary)

        line = 1

        self.window.addstr(line, 1, "Liste: ", A_BOLD)
        self.window.addstr(todo.list)
        line += 1

        self.window.addstr(line, 1, "Priority: ", A_BOLD)
        text, color = Formater.formatPriority(todo.priority)
        self.window.addstr(text, color)
        line += 1

        if todo.completed:
            self.window.addstr(line, 1, "Completed: ", A_BOLD)
            self.window.addstr(
                f"{todo.completed.strftime(str(Config.get("UI", "date_format")))}"
            )
            line += 1

        if todo.due:
            self.window.addstr(line, 1, "Due: ", A_BOLD)
            init_pair(21, COLOR_RED, -1)
            local_tz = get_locale_tz()
            color = 21 if todo.due.replace() > datetime.now(local_tz) else -1
            self.window.addstr(
                f"{todo.due.strftime(str(Config.get("UI", "date_format")))}"
            )
            # self.window.addstr(f" {todo.due.humanize()}", color_pair(21))
            line += 1

        if todo.categories and len(todo.categories) > 0:
            self.window.addstr(line, 1, "Categories: ", A_BOLD)
            self.window.addstr("".join(todo.categories or []))
            line += 1

        if todo.location and len(todo.location) > 0:
            self.window.addstr(line, 1, "Location: ", A_BOLD)
            self.window.addstr(todo.location)
            line += 1

        if todo.description:
            draw_line(self.window, line, self.length)
            line += 1
            self.window.addstr(line, 1, "Description: ", A_BOLD)
            line += 1
            i = 0
            for i, description_line in enumerate(todo.description.splitlines()):
                self.window.addstr(line + i, 1, description_line)
            line = line + i

        self.window.refresh()

    def main_loop(self) -> None:
        while True:
            k = self.window.getch()
            if self.controller.handle_key(k):
                break
