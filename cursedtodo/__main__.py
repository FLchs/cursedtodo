from curses import (
    A_NORMAL,
    A_STANDOUT,
    curs_set,
    endwin,
    error,
    newpad,
    newwin,
    start_color,
    use_default_colors,
    window,
    wrapper,
)

from cursedtodo.models.todolist import TodoList
from cursedtodo.presenters.todolist import TodoListPresenter

# from cursedtodo.utils.config import Config
from cursedtodo.views.todolist import TodoListView


def main(stdscr: window) -> None:
    start_color()
    use_default_colors()
    curs_set(0)
    stdscr.refresh()
    view = TodoListView()
    presenter = TodoListPresenter(stdscr, view)
    presenter.run()

    # # Sample data: a list of numbers
    # data = TodoList.get_list(True)
    # height, width = stdscr.getmaxyx()
    # pad_height = len(data)
    #
    # # Create a pad that is larger than the screen
    # window = newwin(height, width, 0, 0)
    # window.box()
    # window.refresh()
    # pad = newpad(pad_height, width)
    #
    # # Initial position
    # top = 0
    # current = 0
    # order = True
    #
    # def draw():
    #     # Display the data in the pad
    #     pad.clear()
    #     for i, item in enumerate(data):
    #         pad.addstr(i, 0, item.summary, A_STANDOUT if i == current else A_NORMAL)
    #
    # draw()
    # while True:
    #     # stdscr.clear()
    #     # Show the pad on the screen
    #     # stdscr.refresh()
    #     # window.box()
    #     # window.refresh()
    #     pad.refresh(top, 0, 1, 2, height - 2, width - 1)
    #     key = stdscr.getch()
    #
    #     if key == ord("q"):
    #         break
    #     elif key == ord("o"):
    #         data.sort(key=lambda x: x.priority, reverse=order)
    #         order = not order
    #         draw()
    #         pad.refresh(top, 0, 1, 2, height - 2, width - 1)
    #     elif key == ord("j"):
    #         # Move down
    #         # if current + 1 < height:
    #         if current < len(data) - 1:
    #             current += 1
    #             if current + 1 > height - 2:
    #                 # Scroll down
    #                 top += 1
    #                 if top + height - 2 > pad_height:
    #                     top = pad_height - height
    #             draw()
    #         pad.refresh(top, 0, 1, 2, height - 2, width - 1)
    #     elif key == ord("k"):
    #         # Move up
    #         if current > 0:
    #             current -= 1
    #             if current < top:
    #                 # Scroll up
    #                 top -= 1
    #                 if top < 0:
    #                     top = 0
    #             draw()
    #             pad.refresh(top, 0, 1, 2, height - 2, width - 1)
    #


if __name__ == "__main__":
    wrapper(main)
    # data = Config.get("MAIN", "name")
    # print(data)
