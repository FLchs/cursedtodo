from cursedtodo.controlers.base_controller import Controller
from cursedtodo.models.todo_repository import TodoRepository
from cursedtodo.views.main_view import MainView


class MainController(Controller):
    def run(self) -> None:
        view = MainView(self)
        self.window.clear()
        self.get_data()
        view.render()
        view.main_loop()

    def get_data(self) -> None:
        self.data = TodoRepository.get_list()

    def handle_key(self, key: int) -> bool:
        if key == ord("q"):
            return True
        return False
