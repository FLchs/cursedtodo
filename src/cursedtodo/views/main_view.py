from __future__ import annotations

from curses import newpad, window
import curses
from typing import TYPE_CHECKING

from cursedtodo.models.todo import Todo
from cursedtodo.utils.formater import Formater
from cursedtodo.views.base_view import BaseView

if TYPE_CHECKING:
    from cursedtodo.controlers.main_controller import MainController


class MainView(BaseView):
    def __init__(self, controller: MainController) -> None:
        super().__init__(controller)
        self.controller = controller
        self.index = 0
        self.selected = 0
        self.height, self.length = self.window.getmaxyx()

    def render(self) -> None:
        self.window.erase()
        self.window.box()
        self.window.addstr(0, 5, "Todos")
        self.window.addstr(self.height -1, 5, " q : quit | c: show completed | o : change order")
        self.window.refresh()
        self.render_content()

    def render_line(self, pad: window, y: int, todo: Todo) -> None:
        pad.addstr(y, 0, todo.list)
        pad.addstr(y, 10, todo.summary)
        text, color = Formater.formatPriority(todo.priority)
        pad.addstr(y, 70, text,  color)
        if y == self.selected:
            pad.chgat(y, 0, self.length, curses.A_STANDOUT)

    def render_content(self) -> None:
        self.pad = newpad(5000, self.length)
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
