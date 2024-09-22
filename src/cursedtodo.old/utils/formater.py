import curses


class Formater:

    @staticmethod
    def formatPriority(priority: int) -> tuple[str, int]:

        # Ensure the priority is within the valid range
        if priority < 0 or priority > 9:
            raise ValueError("Priority must be between 0 and 9")

        # Define words and colors based on priority
        words = [
            "Lowest",
            "Very Low",
            "Low",
            "Below Average",
            "Average",
            "Above Average",
            "High",
            "Very High",
            "Highest",
            "Critical",
        ]
        colors = [
            curses.COLOR_WHITE,
            curses.COLOR_BLUE,
            curses.COLOR_CYAN,
            curses.COLOR_GREEN,
            curses.COLOR_YELLOW,
            curses.COLOR_MAGENTA,
            curses.COLOR_RED,
            curses.COLOR_RED,
            curses.COLOR_RED,
            curses.COLOR_RED,
        ]

        # Initialize color pairs
        curses.start_color()
        for i, color in enumerate(colors):
            curses.init_pair(i + 10, color, curses.COLOR_BLACK)

        # Get the word and color for the given priority
        word = words[priority]
        color_pair = curses.color_pair(priority + 10)
        return word, color_pair
