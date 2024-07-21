import curses
from dataclasses import dataclass

from cursedtodo.todo import Todo


@dataclass
class TodoItem:

    @staticmethod
    def display(todo: Todo, num_rows: int, num_cols: int):
        info = curses.newwin(num_rows, num_cols, 0, 0)
        info.box()
        info.addstr(1, 1, "Id:")
        info.addstr(1, 21, str(todo.id))
        info.addstr(2, 1, "List:")
        info.addstr(2, 21, todo.list)
        info.addstr(3, 1, "Summary:")
        info.addstr(3, 21, todo.summary)
        info.refresh()
