from dataclasses import dataclass

from cursedtodo.utils.colors import BLUE, CYAN, GREEN, MAGENTA, RED, WHITE, YELLOW


@dataclass
class Priority:
    index: int
    value: str
    color: int


class Formater:
    priorities = [
        Priority(0, "No priority", WHITE),
        Priority(9, "Very Low", BLUE),
        Priority(8, "Low", CYAN),
        Priority(7, "Below Average", GREEN),
        Priority(6, "Average", YELLOW),
        Priority(5, "Above Average", MAGENTA),
        Priority(4, "High", RED),
        Priority(3, "Very High", RED),
        Priority(2, "Highest", RED),
        Priority(1, "Critical", RED),
    ]

    @staticmethod
    def formatPriority(priority: int) -> tuple[str, int]:
        # Ensure the priority is within the valid range
        if priority < 0 or priority > 9:
            raise ValueError("Priority must be between 0 and 9")

        # Get the word and color for the given priority
        fmt_priority = next(p for p in Formater.priorities if p.index == priority)
        return fmt_priority.value, fmt_priority.color

    @staticmethod
    def parse_priority(string: str | None) -> int:
        if string is None:
            return 0
        return next(p for p in Formater.priorities if p.value == string).index or 0
