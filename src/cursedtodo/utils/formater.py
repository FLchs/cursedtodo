import curses
from dataclasses import dataclass


@dataclass
class Priority:
    index: int
    value: str
    color: int


class Formater:
    priorities = [
        Priority(0, "No priority", curses.COLOR_WHITE),
        Priority(10, "Lowest", curses.COLOR_WHITE),
        Priority(9, "Very Low", curses.COLOR_BLUE),
        Priority(8, "Low", curses.COLOR_CYAN),
        Priority(7, "Below Average", curses.COLOR_GREEN),
        Priority(6, "Average", curses.COLOR_YELLOW),
        Priority(5, "Above Average", curses.COLOR_MAGENTA),
        Priority(4, "High", curses.COLOR_RED),
        Priority(3, "Very High", curses.COLOR_RED),
        Priority(2, "Highest", curses.COLOR_RED),
        Priority(1, "Critical", curses.COLOR_RED),
    ]

    @staticmethod
    def init_priority_colors() -> None:
        # Initialize color pairs for each priority
        for priority in Formater.priorities:
            curses.init_pair(10 + priority.index, priority.color, -1)


    @staticmethod
    def formatPriority(priority: int) -> tuple[str, int]:
        # Ensure the priority is within the valid range
        if priority < 0 or priority > 9:
            raise ValueError("Priority must be between 0 and 9")


        # Get the word and color for the given priority
        fmt_priority = next(p for p in Formater.priorities if p.index == priority)
        return fmt_priority.value, curses.color_pair(fmt_priority.index + 10)

    @staticmethod
    def parse_priority(string: str | None) -> int:
        if string is None:
            return 0
        return next(p for p in Formater.priorities if p.value == string).index or 0
