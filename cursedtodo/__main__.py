import curses

from cursedtodo.data import Data
from cursedtodo.ui.screen import Screen
from cursedtodo.ui.todoitem import TodoItem
from cursedtodo.ui.todolist import TodoList


def main():

    main = Screen()
    screen = main.screen

    num_cols = main.num_cols
    num_rows = main.num_rows

    window = TodoList(rows=num_rows - 1, cols=num_cols)
    data = Data.loadTodos()
    window.draw(data)

    order = False
    k = 0
    while k != ord("q"):
        k = screen.getch()
        if k == curses.KEY_DOWN or k == ord("j"):
            window.selected = min(window.selected + 1, len(data) - 1)
        elif k == curses.KEY_UP or k == ord("k"):
            window.selected = max(window.selected - 1, 0)
        elif k == curses.KEY_UP or k == ord("o"):
            order = not order
            data.sort(key=lambda x: x.priority, reverse=order)
        elif k == curses.KEY_ENTER or k == 10 or k == 13:
            TodoItem.display(data[window.selected], num_rows - 1, num_cols)
            screen.getch()
        main.refresh()
        window.draw(data)

    curses.endwin()


if __name__ == "__main__":
    main()
