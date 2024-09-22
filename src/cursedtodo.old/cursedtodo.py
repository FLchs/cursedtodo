from curses import curs_set, start_color, use_default_colors, window, wrapper

from cursedtodo.presenters.todolist import TodoListPresenter
from cursedtodo.views.todolist import TodoListView


def cursedtodo(stdscr: window) -> None:
    start_color()
    use_default_colors()
    curs_set(0)
    stdscr.refresh()
    view = TodoListView()
    presenter = TodoListPresenter(stdscr, view)
    presenter.run()


def main():
    wrapper(cursedtodo)


if __name__ == "__main__":
    main()
