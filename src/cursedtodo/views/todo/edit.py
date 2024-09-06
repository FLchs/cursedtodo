import curses
from curses import A_BOLD, A_NORMAL, A_REVERSE, newwin

from cursedtodo.models.todo import Todo
from cursedtodo.models.todolist import TodoList
from cursedtodo.views.todo.confirm import Confirm
from cursedtodo.views.todo.field.selectField import SelectField
from cursedtodo.views.todo.field.textField import TextField as TestField


class EditTodoView:

    def __init__(self):
        pass

    def init(self, presenter):
        self.presenter = presenter
        self.todo = presenter.todo
        (self.rows, self.cols) = self.presenter.stdscr.getmaxyx()
        self.window = newwin(self.rows, self.cols, 0, 0)
        self.window.clear()
        self.window.box()
        self.current_field = 0
        self.inputs = []
        self.values = [self.todo.summary, str(self.todo.priority), self.todo.list]

    def validator(self, ch):

        # if ch == 9:  # Tab key
        #     current_field = current_field + 1
        #     return 7  # Stop editing

        if ch == 10 or ch == 9:
            if self.current_field > len(self.inputs) + 2:
                self.current_field = 0
            else:
                self.current_field += 1
            return 7
        return ch

    def render(self=None):
        self.window.refresh()
        self.inputs.append(TestField("Summary", 0, self.validator, self.values[0]))
        self.inputs.append(TestField("Priority", 1, self.validator, self.values[1]))
        self.inputs.append(
            SelectField(
                "List", 2, self.validator, TodoList.get_lists_names(), self.values[2]
            )
        )

        self.save_button_win = curses.newwin(1, 5, 1 + len(self.values), 1)
        self.save_button_win.addstr(0, 0, "Save", curses.A_BOLD)
        self.cancel_button_win = curses.newwin(1, 9, 1 + len(self.values), 6)
        self.cancel_button_win.addstr(0, 0, "Cancel", curses.A_BOLD)
        return self.main_loop()

    def main_loop(self):
        for input in self.inputs:
            input.render()

        while True:
            self.save_button_win.attroff(A_NORMAL)
            self.save_button_win.refresh()
            self.cancel_button_win.attroff(A_NORMAL)
            self.cancel_button_win.refresh()
            if self.current_field < len(self.inputs):
                curses.curs_set(1)
                id = self.current_field
                self.values[id] = self.inputs[id].gather()
            elif self.current_field == len(self.inputs):
                curses.curs_set(0)
                self.save_button_win.chgat(0, 0, A_REVERSE)
                while True:
                    k = self.save_button_win.getch()
                    if k == 9:
                        self.current_field += 1
                        self.save_button_win.chgat(0, 0, A_BOLD)
                        break
                    elif k == 10:
                        self.current_field += 1
                        return self.values
            elif self.current_field > len(self.inputs):
                curses.curs_set(0)
                self.cancel_button_win.chgat(0, 0, A_REVERSE)
                while True:
                    k = self.cancel_button_win.getch()
                    if k == 9:
                        self.current_field = 0
                        self.cancel_button_win.chgat(0, 0, A_BOLD)
                        break
                    elif k == 10:
                        return
