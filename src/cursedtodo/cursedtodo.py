from curses import curs_set, window, wrapper
import curses
import sys
from cursedtodo.utils.router import Router


def app(stdscreen: window) -> None:
    curs_set(0)
    curses.use_default_colors()
    router = Router(stdscreen)
    router.route_main()


def main() -> None:
    try:
        wrapper(app)
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
