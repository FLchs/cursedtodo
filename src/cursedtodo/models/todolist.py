import glob
import os

from ics import Calendar

from cursedtodo.models.todo import Todo
from cursedtodo.utils.config import Config


class TodoList:
    @staticmethod
    def get_list(show_completed=False, asc=False) -> list[Todo]:
        # calendar_dir = os.path.expanduser("~/.local/share/vdirsyncer/calendar/*")
        calendar_dir = os.path.expanduser(
            str(Config.getstr("", "MAIN", "calendars") or "").strip()
        )
        ics_files = glob.glob(os.path.join(calendar_dir, "*.ics"))

        events_todos = [
            Todo(
                event.uid,
                event.name,
                event.description,
                next((x.value for x in event.extra if x.name == "CATEGORIES"), None),
                os.path.basename(os.path.dirname(ics_file)),
                ics_file,
                event.priority or 0,
                event.completed is not None,
            )
            for ics_file in ics_files
            for event in Calendar(open(ics_file).read()).todos
            if event.completed is None or show_completed
        ]

        return sorted(events_todos, reverse=not asc)

    @staticmethod
    def get_lists_names() -> list[str]:
        calendar_dir = os.path.expanduser("~/.local/share/vdirsyncer/calendar")
        return [
            entry.name
            for entry in os.scandir(calendar_dir)
            if not entry.name.startswith(".") and entry.is_dir()
        ]
