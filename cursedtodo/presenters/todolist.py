from curses import window

from cursedtodo.models.todolist import TodoList


class TodoListPresenter:
    def __init__(self, stdscr: window, view):
        self.stdscr = stdscr
        self.view = view
        self.orderPriorityAsc = False
        self.showCompleted = False

    def run(self):
        self.view.todo_list = TodoList.get_list(self.showCompleted, self.showCompleted)
        self.view.init(self)

    def refreshTodoList(self):
        self.view.todo_list = TodoList.get_list(self.showCompleted, self.showCompleted)

    def toggleShowCompleted(self):
        self.showCompleted = not self.showCompleted
        self.view.todo_list = TodoList.get_list(
            self.showCompleted, self.orderPriorityAsc
        )

    def toggleOrderByPriority(self):
        self.orderPriorityAsc = not self.orderPriorityAsc
        self.view.todo_list = TodoList.get_list(
            self.showCompleted, self.orderPriorityAsc
        )
        # self.view.todo_list.sort(
        #     key=lambda x: x.priority, reverse=self.orderPriorityAsc
        # )
