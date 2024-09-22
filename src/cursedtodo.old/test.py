import curses
from curses import panel

def main(stdscr):
    curses.curs_set(0)  # Hide cursor

    # Create main window and subwindows
    win1 = curses.newwin(10, 40, 2, 5)
    win1.box()
    win1.addstr(1, 1, "Window 1")

    win2 = curses.newwin(10, 40, 4, 10)
    win2.box()
    win2.addstr(1, 1, "Window 2")

    # Create panels from windows
    panel1 = panel.new_panel(win1)
    panel2 = panel.new_panel(win2)

    # Stack win2 above win1
    panel2.top()

    # Display all panels (in the correct order)
    panel.update_panels()
    curses.doupdate()
    
    stdscr.getch()
    # Stack win2 above win1
    panel1.top()
    panel.update_panels()
    curses.doupdate()

    stdscr.getch()

curses.wrapper(main)
