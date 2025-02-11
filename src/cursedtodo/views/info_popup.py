from curses import KEY_RESIZE, window, error
from typing import Callable


from cursedtodo.utils.window_utils import add_borders


class InfoPopup:
    @staticmethod
    def show(
        window: window, text: list[str | tuple[str, int]], on_resize: Callable[[], None]
    ) -> bool:
        window = window
        text = text
        height, length = window.getmaxyx()
        max_length = 0
        for line in text:
            max_length = max(max_length, len(line))

        dialog_width = max(max_length + 4, 50)
        dialog = window.derwin(
            len(text) + 2,
            dialog_width,
            (height // 2) - (len(text) // 2),
            (length // 2) - (dialog_width // 2),
        )
        dialog.box()
        try:
            for i, line in enumerate(text):
                if type(line) is tuple:
                    dialog.addstr(i + 1, 2, line[0], line[1])
                elif type(line) is str:
                    dialog.addstr(i + 1, 2, line)
        except error:
            pass
        add_borders(dialog)
        while True:
            k = dialog.getch()
            if k == KEY_RESIZE:
                on_resize()
                return InfoPopup.show(window, text, on_resize)
            elif k == ord("q"):
                return False
