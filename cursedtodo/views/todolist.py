import curses
from itertools import accumulate
from typing import List

from cursedtodo.models.todo import Todo
from cursedtodo.presenters.todo.editTodoPresenter import EditTodoPresenter
from cursedtodo.utils.config import Config
from cursedtodo.utils.formater import Formater
from cursedtodo.views.todo.confirm import Confirm
from cursedtodo.views.todo.edit import EditTodoView


class TodoListView:
    def __init__(self) -> None:
        self.title = "TODO"
        self.cols_widths: List[int] = []
        self.cols_pos: List[int] = []
        self.selected = 0 if Config.get("UI", "select_first") == "True" else -1
        self.top_line = 0
        self.bottom_padding = 0
        # self.presenter = None
        self.todo_list: List[Todo] = []

    def init(self, presenter) -> None:
        self.presenter = presenter
        conf_widths = Config.get("Columns", "widths")
        if conf_widths == None:
            raise Exception("No columns widths in config")
        self.cols_widths = [int(width.strip()) for width in conf_widths.split(",")]
        self.cols_pos = list(accumulate(self.cols_widths))
        # curses.init_pair(66, 0, curses.COLOR_GREEN)
        self.render()
        self.main_loop()

    def render(self) -> None:
        self.presenter.stdscr.clear()
        self.rows, self.cols = self.presenter.stdscr.getmaxyx()
        if Config.getboolean("UI", "show_footer_keybindings") == True:
            self.bottom_padding = 1
            self.draw_footer()
        self.window = curses.newwin(self.rows - self.bottom_padding, self.cols, 0, 0)
        # self.window.attrset(curses.color_pair(1))
        self.window.box()
        # self.window.attrset(curses.color_pair(0))
        self.draw_headers()
        self.window.refresh()
        self.pad = curses.newpad(
            len(self.todo_list), self.cols - 1 - self.bottom_padding
        )
        self.render_list()

    def draw_headers(self):
        window = self.window
        y, x = 1, 1
        columns_names = ["List", "Summary", "Priority"]
        for i, col_name in enumerate(columns_names):
            window.addstr(y, x, col_name, curses.A_BOLD)
            x += self.cols_widths[i]

    def draw_footer(self):
        self.presenter.stdscr.addstr(
            self.rows - 1,
            1,
            "q: quit | o: change order | c: show completed | e: edit todo | a: add todo | x: delete todo",
            curses.A_DIM,
        )
        self.presenter.stdscr.refresh()

    def render_list(self) -> None:
        # self.pad.resize(len(self.todo_list), self.cols - 2)
        self.pad.clear()
        for i, todo in enumerate(self.todo_list):
            word, color = Formater.formatPriority(todo.priority)
            self.pad.addstr(i, 0, todo.list)
            self.pad.addstr(
                i,
                self.cols_pos[0],
                todo.summary,
            )
            self.pad.addstr(i, self.cols_pos[1], word, color)
            if self.selected == i:
                self.pad.chgat(i, 0, self.cols - 2, curses.A_STANDOUT)
            if todo.completed:
                self.pad.chgat(i, 0, self.cols - 2, curses.A_BOLD)
        self.pad.refresh(
            self.top_line, 0, 2, 1, self.rows - 2 - self.bottom_padding, self.cols - 2
        )

    def select_down(self):
        if self.selected < len(self.todo_list) - 1:
            self.selected += 1
            if self.selected >= self.top_line + self.rows - 3 - self.bottom_padding:
                self.top_line += 1
            self.render_list()

    def select_up(self):
        if self.selected > 0:
            self.selected -= 1
            if self.selected < self.top_line:
                self.top_line -= 1
            self.render_list()

    def filter_done(self):
        self.presenter.toggleShowCompleted()
        self.window.redrawwin()
        self.window.refresh()
        self.pad.resize(len(self.todo_list), self.cols - 2)
        self.top_line = 0
        self.selected = 0
        self.render_list()

    def toggle_priority_order(self):
        self.presenter.toggleOrderByPriority()
        self.window.redrawwin()
        self.top_line = 0
        self.selected = 0
        self.render_list()

    def main_loop(self):
        while True:
            k = self.window.getch()
            if k == ord("q"):
                break
            elif k == ord("j"):
                self.select_down()
            elif k == ord("k"):
                self.select_up()
            elif k == ord("c"):
                self.filter_done()
            elif k == ord("o"):
                self.toggle_priority_order()
            elif k == ord("e"):
                editTodoView = EditTodoView()
                editTodoPresenter = EditTodoPresenter(
                    self.presenter.stdscr, editTodoView, self.todo_list[self.selected]
                )
                editTodoPresenter.run()
                self.render_list()
            elif k == ord("a"):
                todo = Todo(0, "", "", "", 0, False)
                editTodoView = EditTodoView()
                editTodoPresenter = EditTodoPresenter(
                    self.presenter.stdscr, editTodoView, todo
                )
                editTodoPresenter.run()
                self.presenter.refreshTodoList()
                self.render()
            elif k == ord("x"):
                confirm = Confirm(
                    "Do you really want to delete this todo ?",
                    self.presenter.stdscr,
                )
                if confirm:
                    self.todo_list[self.selected].delete()
                    self.presenter.refreshTodoList()
                    self.render_list()
