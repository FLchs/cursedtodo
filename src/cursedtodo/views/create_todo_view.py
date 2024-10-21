from __future__ import annotations

from abc import ABC, abstractmethod
from curses import A_BOLD, A_NORMAL, A_STANDOUT, KEY_RESIZE, curs_set, textpad, window
from typing import TYPE_CHECKING, Callable


from cursedtodo.utils.window_utils import add_borders
from cursedtodo.views.base_view import BaseView

if TYPE_CHECKING:
    from cursedtodo.controlers.create_todo_controller import CreateTodoController


class CreateTodoView(BaseView):
    def __init__(self, controller: CreateTodoController) -> None:
        super().__init__(controller)
        self.controller = controller
        self.fields: list[Input] = []
        self.values = [""]
        self.height, self.length = self.window.getmaxyx()
        name_field = TextField(2, self.window, "Name", self.validator)
        categories_field = TextField(3, self.window, "Categories", self.validator)
        save_button = Button(self.window, 6, 1, "Save", self.save, self.validator)
        cancel_button = Button(self.window, 6, 6, "Cancel", self.cancel, self.validator)
        self.fields.append(name_field)
        self.fields.append(categories_field)
        self.fields.append(save_button)
        self.fields.append(cancel_button)

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
        self.window.refresh()

    def save(self) -> bool:
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
            if index == len(self.fields):
                index = 0
            if self.fields[index].focus():
                break
            index += 1

class Input(ABC):

    @abstractmethod
    def render(self) -> None:
        pass

    @abstractmethod
    def save(self) -> None:
        pass

    @abstractmethod
    def focus(self) -> bool | None:
        pass

class TextField(Input):
    def __init__(
        self, y: int, window: window, name: str, validator: Callable[[int], int]
    ):
        self.window = window
        self.name = name
        self.y = y
        self.textwindow = window.derwin(1, 50, y, 15)
        self.textbox = textpad.Textbox(self.textwindow, insert_mode=True)
        self.value = ""
        self.validator = validator
        self.render()

    def render(self) -> None:
        self.window.addstr(self.y, 1, f"{self.name}: ", A_BOLD)
        self.textwindow.move(0, 0)
        self.textwindow.addstr(self.value)
        self.textwindow.move(0, max(len(self.value) - 1, 0))
        self.textwindow.refresh()

    def save(self) -> None:
        self.value = self.textbox.gather()

    def focus(self)-> None:
        curs_set(1)
        self.textwindow.move(0, max(len(self.value) - 1, 0))
        self.textbox.edit(self.validator)
        self.value = self.textbox.gather()


class Button(Input):
    def __init__(
        self,
        window: window,
        y: int,
        x: int,
        name: str,
        action: Callable[[], bool],
        validator: Callable[[int], int],
    ) -> None:
        self.window = window
        self.x = x
        self.y = y
        self.name = name
        self.action = action
        self.validator = validator

    def save(self) -> None:
        pass

    def render(self) -> None:
        self.window.addstr(self.y, self.x, self.name)

    def focus(self) -> bool | None:
        curs_set(0)
        while True:
            self.window.chgat(self.y, self.x, len(self.name), A_STANDOUT)
            k = self.window.getch()
            self.validator(k)
            if k == 10:
                return self.action()
            if k == 9:
                self.window.chgat(self.y, self.x, A_NORMAL)
                self.window.refresh()
                break
        return None
