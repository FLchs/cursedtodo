from cursedtodo.views.base_view import BaseView


class MainView(BaseView):
    def show(self):
        self.window.clear()
        self.window.addstr(0, 0, "To-Do List (Press 'a' to add, 'q' to quit)")
        self.window.refresh()
