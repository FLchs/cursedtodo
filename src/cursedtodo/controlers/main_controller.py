from curses import KEY_RESIZE
from cursedtodo.controlers.base_controller import Controller
from cursedtodo.models.todo_repository import TodoRepository
from cursedtodo.views.main_view import MainView


class MainController(Controller):
    def run(self) -> None:
        self.show_completed = False
        self.asc = False
        self.view = MainView(self)
        self.window.clear()
        self.get_data()
        self.view.render()
        self.view.main_loop()

    def get_data(self) -> None:
        self.data = TodoRepository.get_list(self.show_completed)

    def handle_key(self, key: int) -> bool:
        if key == KEY_RESIZE:
            self.view.render()
        if key == ord("q"):
            return True
        if key == ord("c"):
            self.view.selected = 0
            self.view.index = 0
            self.show_completed = not self.show_completed
            self.data = TodoRepository.get_list(self.show_completed, self.asc)
        if key == ord("o"):
            self.view.selected = 0
            self.view.index = 0
            self.asc = not self.asc
            self.data = TodoRepository.get_list(self.show_completed, self.asc)
        return False
