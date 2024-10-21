from curses import window
import curses

from cursedtodo.utils.config import Config


def add_borders(window: window) -> None:
    max_y, max_x = window.getmaxyx()
    # Can't directly use chars in box() or border() beceause of utf8 
    try:
        window.box()
        if  bool(Config.get("UI", "rounded_borders")):
            window.addch(0, max_x - 1, "╮")
            window.addch(0, 0, "╭")
            window.addch(max_y - 1, 0, "╰")
            window.addch(max_y - 1, max_x - 1, "╯")
    except Exception:
        pass

def draw_line(window: window, y:int, max_x: int) -> None:
    window.addch(y, 0, "├")
    window.hline(curses.ACS_HLINE, max_x-2)
    window.addch(y, max_x-1,"┤")
