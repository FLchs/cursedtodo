from curses import curs_set, window, wrapper
import curses
from cursedtodo.utils.router import Router

def app(stdscreen: window) -> None:
    curs_set(0)
    curses.use_default_colors()
    router = Router(stdscreen)
    router.route_main()

def main() -> None:
    wrapper(app)
    
if __name__ == "__main__":
    main()
