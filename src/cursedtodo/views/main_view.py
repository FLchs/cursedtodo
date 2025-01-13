from __future__ import annotations

import curses
from curses import newpad, window
from datetime import datetime
from operator import attrgetter
from typing import TYPE_CHECKING

from cursedtodo.config import Config
from cursedtodo.models.todo import Todo
from cursedtodo.utils.colors import RED, WHITE, random_color
from cursedtodo.utils.formater import Formater
from cursedtodo.utils.time import get_locale_tz
from cursedtodo.utils.window_utils import add_borders
from cursedtodo.views.base_view import BaseView

if TYPE_CHECKING:
    from cursedtodo.controlers.main_controller import MainController


class MainView(BaseView):
    def __init__(self, controller: MainController) -> None:
        super().__init__(controller)
        self.controller = controller
        self.index = 0
        self.selected = 0

    def render(self) -> None:
        self.height, self.length = self.window.getmaxyx()
        self.window.erase()
        add_borders(self.window)
        self.window.addstr(0, 5, Config.ui.window_name)
        self.window.addstr(
            self.height - 1,
            5,
            " q : quit | c: show completed | o : change order | space : mark as done | x: delete ",
        )
        self.window.refresh()
        self.pad = newpad(max(len(self.controller.data), self.length), self.length)
        self.render_content()

    def render_line(self, pad: window, y: int, todo: Todo) -> None:
        columns = Config.columns
        pad.move(y, 0)
        for column in columns:
            content = ""
            attr = 0
            if column.property == "priority" and todo.priority > 0:
                content, attr = Formater.formatPriority(todo.priority)
            elif column.property == "due" and todo.due is not None:
                local_tz = get_locale_tz()
                attr = RED if todo.due.replace() > datetime.now(local_tz) else -1
                content = f"{todo.due.strftime(Config.ui.date_format)}"
            elif column.property == "calendar.name":
                content = todo.calendar.name
                attr = todo.calendar.color_attr
            elif column.property == "categories" and todo.categories:
                content = ", ".join(todo.categories or [])
                for category in todo.categories:
                    color = (
                        random_color(category) if Config.ui.category_colors else WHITE
                    )
                    pad.addstr(f"{category} ", color)
                continue
            else:
                getter = attrgetter(column.property)
                content = str(getter(todo) or "")
            pad.addstr(content[: column.width - 1].ljust(column.width), attr)
        if todo.completed:
            pad.chgat(y, 0, self.length, curses.A_DIM)
        if y == self.selected:
            pad.chgat(y, 0, self.length, curses.A_STANDOUT)

    def render_content(self) -> None:
        self.pad.erase()
        self.pad.resize(max(len(self.controller.data), self.length), self.length)
        if self.height - self.selected > self.index:
            self.index = self.selected - self.height + 3
        for i, todo in enumerate(self.controller.data):
            self.render_line(self.pad, i, todo)
        self.pad.refresh(self.index, 0, 1, 1, self.height - 2, self.length - 2)

    def main_loop(self) -> None:
        while True:
            k = self.pad.getch()
            if self.controller.handle_key(k):
                break
            elif k == ord("j") and self.selected < len(self.controller.data) - 1:
                self.selected += 1
                if self.selected > self.height - 3:
                    self.index += 1
            elif k == ord("k") and self.selected > 0:
                self.selected -= 1
                if self.selected < self.index:
                    self.index -= 1
            self.render_content()
