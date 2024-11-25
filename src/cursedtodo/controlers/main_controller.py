from curses import KEY_RESIZE

from cursedtodo.controlers.base_controller import Controller
from cursedtodo.models.todo_repository import TodoRepository
from cursedtodo.views.dialog import Dialog
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
        if key == 10:
            self.router.route_view_todo(self.data[self.view.selected])
            self.data = TodoRepository.get_list(self.show_completed, self.asc)
            self.view.render()
        if key == ord("e"):
            self.router.route_edit_todo(self.data[self.view.selected])
            self.view.render()
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
        if key == ord("n"):
            self.router.route_create_todo()
            self.data = TodoRepository.get_list(self.show_completed, self.asc)
            self.view.render()
        if key == 32:
            todo = self.data[self.view.selected]
            todo.mark_as_done()
            TodoRepository.save(todo)
            self.data = TodoRepository.get_list(self.show_completed, self.asc)
            if not self.show_completed and todo.completed is not None:
                self.data.append(todo)
            self.view.selected = 0
            self.view.render()
        if key == ord("x"):
            result = Dialog.confirm(
                self.window,
                "This action will permanently delete the item. Are you sure you want to proceed?",
                self.view.render,
            )
            if result:
                TodoRepository.delete(self.data[self.view.selected])
                self.data = TodoRepository.get_list(self.show_completed, self.asc)
            self.view.render()
        return False
