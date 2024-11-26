from curses import A_NORMAL, A_STANDOUT, KEY_RESIZE, window
from typing import Callable


from cursedtodo.utils.window_utils import add_borders, draw_line


class Dialog:
    @staticmethod
    def confirm(window: window, text: str, on_resize: Callable) -> bool:
        window = window
        text = text
        height, length = window.getmaxyx()
        dialog_width = max(len(text) + 4, 50)
        dialog = window.derwin(
            6,
            dialog_width,
            (height // 2) - 3,
            (length // 2) - (dialog_width // 2),
        )
        dialog.box()
        add_borders(dialog)
        dialog.addstr(1, 1, text.center(dialog_width - 2))
        draw_line(dialog, 3, dialog_width)
        dialog.addstr(4, dialog_width - 9 - 9, "[ Ok ]")
        dialog.addstr(4, dialog_width - 2 - 9, "[ Cancel ]")
        index = 1
        dialog.chgat(4, dialog_width - 2 - 6 - 10, 6, A_STANDOUT)
        while True:
            k = dialog.getch()
            if k == KEY_RESIZE:
                on_resize()
                return Dialog.confirm(window, text, on_resize)
            elif k == 9 or k == ord("h") or k == ord("l"):
                dialog.chgat(4, 1, dialog_width - 2, A_NORMAL)
                if index == 0:
                    dialog.chgat(4, dialog_width - 2 - 6 - 10, 6, A_STANDOUT)
                else:
                    dialog.chgat(4, dialog_width - 11, 10, A_STANDOUT)
                index = index ^ 1
            elif k == 10:
                return index == 1
            elif k == ord("q"):
                return False
