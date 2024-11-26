from __future__ import annotations

import curses
from curses import newpad, window
from typing import TYPE_CHECKING

from cursedtodo.models.todo import Todo
from cursedtodo.utils.formater import Formater
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
        self.window.addstr(0, 5, "Todos")
        self.window.addstr(
            self.height - 1,
            5,
            " q : quit | c: show completed | o : change order | space : mark as done | d: delete",
        )
        self.window.refresh()
        self.pad = newpad(max(len(self.controller.data), self.length), self.length)
        Formater.init_priority_colors()
        self.render_content()

    def render_line(self, pad: window, y: int, todo: Todo) -> None:
        columns = [10, min(self.length - 16, 70), 20, 25]
        summary = (
            (todo.summary[: columns[1] - 12] + "…")
            if len(todo.summary) > columns[1] - 12
            else todo.summary
        )
        pad.addnstr(y, 0, todo.list.ljust(columns[0]), columns[0])
        pad.addnstr(summary.ljust(columns[1]), columns[1])
        text, color = Formater.formatPriority(todo.priority) if todo.priority >0 else ("", 0)
        pad.addnstr(text.ljust(columns[2]), columns[2], color)
        pad.addnstr(str(todo.due or "").ljust(columns[3]), columns[3])
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
