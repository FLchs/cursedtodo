from cursedtodo.views.base_view import BaseView


class ShowTodoView(BaseView):
    def show(self):
        self.window.clear()
        self.window.addstr(1, 0, "To-Do ITEM THIS TIME (Press 'a' to add, 'q' to quit)")
        self.window.refresh()
