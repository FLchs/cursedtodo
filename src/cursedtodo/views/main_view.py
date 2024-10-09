from __future__ import annotations
from typing import TYPE_CHECKING
from cursedtodo.views.base_view import BaseView

if TYPE_CHECKING:
    from cursedtodo.controlers.main_controller import MainController



class MainView(BaseView):
    def __init__(self, controller: MainController) -> None:
        super().__init__(controller)
        self.controller = controller
        self.count = 0

    def render(self) -> None:
        self.window.erase()
        self.window.addstr(0, 0, "Main window")
        self.window.addstr(1, 0, str(self.count))
        self.window.addstr(2,0, self.controller.data[self.count].summary)

    def main_loop(self) -> None:
        while True:
            k = self.window.getch()
            if self.controller.handle_key(k):
                break
            elif k == ord("k") and self.count < len(self.controller.data) -1:
                self.count += 1
            elif k == ord("j") and self.count > 0:
                self.count -= 1
            self.render()
