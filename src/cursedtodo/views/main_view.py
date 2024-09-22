from typing import Any
from cursedtodo.views.base_view import BaseView


class MainView(BaseView):
    def __init__(self, controler: Any) -> None:
        super().__init__(controler)
        self.count = 0

    def render(self) -> None:
        self.window.erase()
        self.window.addstr(0, 0, "Main window")
        self.window.addstr(1, 0, str(self.count))
        self.window.addstr(2,0, self.controller.data[0].summary)

    def main_loop(self) -> None:
        while True:
            k = self.window.getch()
            if self.controller.handle_key(k):
                break
            elif k == ord("k"):
                self.count += 1
            elif k == ord("j"):
                self.count -= 1
            self.render()
