from curses import wrapper

from cursedtodo.screens import navigator

def cursedtodo(stdscr):
    navigator.screen = stdscr
    navigator.todo_list()

def main():
    wrapper(cursedtodo)


if __name__ == "__main__":
    main()
